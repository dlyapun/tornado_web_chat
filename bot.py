# coding=utf-8
# author: dlyapun

import requests
import re
import json
import urllib2

# Way for Yandex API (Live ver4)
URL_LAST_NEWS = 'https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty'
URL_NAME_GEN = 'http://api.namefake.com/'
NEWS_COUNT = 3


class ChatBot(object):

    def __init__(self):
        self.name = 'Skynet'

    def get_bot_name(self):
        return self.name

    def set_bot_name(self, new_name):
        self.name = new_name

    def get_random_name(self):
        r = requests.get(URL_NAME_GEN)
        self.name = r.json()['name']

    def post_reuest(self):
        data = {
            'method': 'method',
            'token': 'token',
            'param': 'simple param'
        }

        r = requests.post(URL, data=json.dumps(data))

    def get_last_news(self):
        r = requests.get(URL_LAST_NEWS)
        list_news = r.text[2:-2].split(',')[:NEWS_COUNT]
        last_news = []
        text = 'Most popular posts with ycombinator:<br>'
        for new in list_news:
            url = 'https://hacker-news.firebaseio.com/v0/item/%s.json?print=pretty' % (
                new.replace(' ', ''))
            r = requests.get(url)
            json = r.json()
            last_news.append(json)
            try:
                url = r.json()['url']
                title = r.json()['title']
            except KeyError:
                continue
            text += "<b>title:</b> " + ("<a href='%s'>%s</a>" % (url, title)) + '<br>'
        return text

    def sum(self, x, y):
        return x + y

    def message_analysis(self, message):
        if message == '/bot get name':
            return "My name is " + self.get_bot_name()

        elif "new posts" in message:
            return self.get_last_news()

        elif "sum" in message:
            numbers = re.findall('(\d+)', message)
            total = 0
            st = 'Sum of '
            for num in numbers:
                total += int(num)
                st += str(num) + ', '
            return st + "= " + str(total)

        elif "div" in message:
            numbers = re.findall('(\d+)', message)
            total = float(numbers[0]) ** 2
            st = 'Divide of '
            for num in numbers:
                total /= float(num)
                st += str(num) + ', '
            return st + "= " + str(total)

        elif "exchange rates" in message:
            return 'test'

        else:
            return "I don't understand you :("
