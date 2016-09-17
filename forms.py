# coding=utf-8


from wtforms.fields import StringField
from wtforms.validators import Required
from wtforms_tornado import Form

class ChannelNameForm(Form):
    name = StringField(u'First Name', validators=[Required()])