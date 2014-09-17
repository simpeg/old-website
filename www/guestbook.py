import cgi
import datetime
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users

import os
import jinja2
import urllib, hashlib

guestbook_key = ndb.Key('Guestbook', 'default_guestbook')



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__).split('/')[:-1])),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)

def setTemplate(self, template_values, templateFile):
    _templateFolder = 'templates/'
    # add Defaults
    template_values['_templateFolder'] = _templateFolder

    path = os.path.normpath(_templateFolder+templateFile)
    template = JINJA_ENVIRONMENT.get_template(path)
    self.response.write(template.render(template_values))




class Greeting(ndb.Model):
    author = ndb.UserProperty()
    content = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        setTemplate(self, {}, 'index.html')


class Guestbook(webapp2.RequestHandler):
    def post(self):
        greeting = Greeting(parent=guestbook_key)

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook)
], debug=True)
