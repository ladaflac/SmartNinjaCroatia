#!/usr/bin/env python
import os
import jinja2
import webapp2
from google.appengine.api import users
from model import Message
import json
from google.appengine.api import urlfetch



template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url("/")
        logout_url = users.create_logout_url("/")
        params = {
            "login_url": login_url,
            "logout_url": logout_url
        }
        if user:
            params["user"] = user
        return self.render_template("hello.html", params = params)

class MessageHandler(BaseHandler):

    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url("/")
        logout_url = users.create_logout_url("/")
        params = {
            "login_url": login_url,
            "logout_url": logout_url
        }
        if user:
            params["user"] = user
        return self.render_template("new_message.html", params = params)

    def post(self):
        sender = self.request.get("from")
        receiver = self.request.get("to")
        subject = self.request.get("subject")
        message = self.request.get("message")
        def status():
            if self.request.get("send"):
                return "S"
            elif self.request.get("draft"):
                return "D"
        email = Message(sender=sender, receiver=receiver, subject=subject, message=message, status=status())
        email.put()
        return self.redirect_to("homepage")

    # todo fetch
    def get(self):
        emails = Message().query().fetch(1)
        return self.render_template("hello.html", params={
            "messages": emails
        })

class WeatherHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url("/")
        logout_url = users.create_logout_url("/")
        params = {
            "login_url": login_url,
            "logout_url": logout_url
        }
    def get(self):
        data = urlfetch.fetch("http://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=4cc018dd25999ae65add9327ac6d8644")
        weather = json.loads(data.content)
        return self.render_template("weather.html", params={
            "prognoza": weather
        })

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="homepage"),
    webapp2.Route('/new_message', MessageHandler),
    webapp2.Route('/weather', WeatherHandler)

], debug=True)
