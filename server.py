# coding=utf-8


from  tornado.escape import json_decode
from  tornado.escape import json_encode
from forms import ChannelNameForm
from pymongo import MongoClient
import datetime
import hashlib
import json
import os.path
import tornado.auth
import tornado.gen
import tornado.ioloop
import tornado.web
import tornado.websocket

# from tornado.options import define, options, parse_command_line
# define('port', default=8000, help='run on the given port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        connection = MongoClient('127.0.0.1', 27017)
        self.db = connection.chat

        handlers = [
            (r'/', MainHandler),
            (r'/channels', SearchHandler),
            (r'/create_channel', CreateChannelHandler),
            (r"/channels/(?P<channel>\w+)", ChannelHandler),
            (r"/channels/(?P<channel>\w+)/", ChannelHandler),
            (r'/ws', WebSocketHandler),
            (r'/login', LoginHandler),
            (r'/sign_up', SignUpHandler),
            (r'/logout', LogoutHandler),
        ]

        settings = dict(
            cookie_secret="12345678",
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            login_url='/login',
            xsrf_cookies=True,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_secure_cookie("username")
        if user:
            user = user.decode("utf-8")
        return user


class MainHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect('/channels')
        self.render('index.html')


class SearchHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # db = self.application.db
        # channels = db.channels.find()
        self.render('channels.html', user=self.current_user, channels=None)

    def post(self):
        channel = self.get_argument('channel')
        db = self.application.db
        channels = db.channels.find({'channel':channel})
        self.render('channels.html', user=self.current_user, channels=channels)


class CreateChannelHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('create_channel.html', title='Create Channel', errors=None)

    def post(self):
        form = ChannelNameForm(self.request.arguments)
        if form.validate():
            channel_name = str(form.data['name'])
            db = self.application.db
            channel_name_db = db.channels.find_one({'channel':channel_name})
            if not channel_name_db:
                db.channels.insert({'channel': channel_name})
                self.redirect('/channels/%s' % channel_name)
            else:
                errors = "Please write another name"
        else:
            errors = "Please write valid name"

        print errors
        self.render('create_channel.html', errors=errors)



class ChannelHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        db = self.application.db
        channel = kwargs.get('channel', 'main')
        channel_db = db.channels.find_one({'channel':channel})
        if not channel_db:
            self.redirect('/channels')

        messages = db.messages.find({'channel': channel})
        self.render('chat.html', user=self.current_user, messages=messages, channel=channel)


class WebSocketHandler(BaseHandler, tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        WebSocketHandler.connections.add(self)

    def on_close(self):
        WebSocketHandler.connections.remove(self)

    def on_message(self, msg):
        db = self.application.db
        date = str(datetime.datetime.utcnow())
        data = json.loads(msg)
        db.messages.insert({'user_name': self.current_user,
                            'date': date,
                            'channel': data['room'],
                            'message': data['msg']})
        self.send_messages(data['msg'], date)

    def send_messages(self, msg, date):
        for conn in self.connections:
            conn.write_message({'name': self.current_user, 'msg': msg, 'date':date})


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html', title='Authentication')

    def post(self):
        password = self.get_argument('password')
        db = self.application.db
        user = db.users.find_one({'user_name':self.get_argument('name')})
        try:
            user_password = user['password']
        except TypeError:
            user_password = None
        
        if str(hashlib.md5(password).hexdigest()) == str(user_password):
            secure_cookie = self.set_secure_cookie('username', user['user_name'])
            self.redirect('/channels')
        else:
            self.render('login.html')


class SignUpHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('sign_up.html', title='Authentication')

    def post(self):
        secure_cookie = self.set_secure_cookie('username', self.get_argument('name'))
        password = self.get_argument('password')
        user_name = self.get_argument('name')
        db = self.application.db
        db.users.insert({'user_name': user_name,
                         'password': hashlib.md5(password).hexdigest(),
                         'last_update': datetime.datetime.utcnow(),
                         'secure_cookie': secure_cookie})
        self.redirect('/login')


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')


def main():
    # parse_command_line()
    port = int(os.environ.get("PORT", 5000))
    app = Application()
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
