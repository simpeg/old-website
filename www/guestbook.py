import cgi
import datetime
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.api import urlfetch

import os
import jinja2
import urllib, hashlib
import json


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



class MainPage(webapp2.RequestHandler):
    def get(self):
        setTemplate(self, {}, 'index.html')


class Why(webapp2.RequestHandler):
    def get(self):
        setTemplate(self, {}, 'why.html')


baseURL = 'http://www.3ptscience.com'

def getJournals():
    url = baseURL + "/api/blogs/group?match=simpeg&brief=True"
    result = urlfetch.fetch(url)
    if not result.status_code == 200:
        return None
    return json.loads(result.content)

class Journals(webapp2.RequestHandler):
    def get(self):
        js = getJournals()
        for i, j in enumerate(js):
            j['index'] = i
        setTemplate(self, {'blogs':js, 'numBlogs':len(js)}, 'journals.html')


def getJournal(uid):
    url = baseURL + "/api/blog/"+uid
    result = urlfetch.fetch(url)
    if not result.status_code == 200:
        return None
    return json.loads(result.content)


class Journal(webapp2.RequestHandler):
    def get(self):
        slug = self.request.path.split('/')[-1]

        j = getJournal(slug)
        if len(j) == 0:
            setTemplate(self, {}, 'error.html')
            return

        j['date'] = datetime.datetime.strptime(j['date'], "%Y-%m-%dT%H:%M:%SZ")
        setTemplate(self, {'blog':j}, 'journal.html')


class Contact(webapp2.RequestHandler):
    def get(self, mailSent=False):
        data = {'mailSent':mailSent}
        setTemplate(self, data, 'contact.html')

    def post(self):
        email   = self.request.get('email')
        name    = self.request.get('name')
        message = self.request.get('message')

        sender_address = "SimPEG Mail <rowanc1@gmail.com>"
        email_to = "Rowan Cockett <rowanc1@gmail.com>"
        email_subject = "SimPEGMail"
        email_message = "New email from:\n\n%s<%s>\n\n\n%s\n" % (name,email,message)

        mail.send_mail(sender_address, email_to, email_subject, email_message)
        self.get(mailSent=True)


class Images(webapp2.RequestHandler):
    def get(self):
        self.redirect('http://www.3ptscience.com'+self.request.path)


class Error(webapp2.RequestHandler):
    def get(self):
        setTemplate(self, {}, 'error.html')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/journal', Journals),
    ('/why', Why),
    ('/journal/.*', Journal),
    ('/img/.*', Images),
    ('/contact', Contact),
    ('/.*', Error),
], debug=os.environ.get("SERVER_SOFTWARE", "").startswith("Dev"))
