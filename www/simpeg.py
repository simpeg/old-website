
import os
import sys

sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))

import cgi
import datetime
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.api import urlfetch

import jinja2
import urllib
import hashlib
import json
import markdown

import requests
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

from article import GistArticle, add_contributors


with open("contributors.json", "r") as f:
    add_contributors(json.loads(f.read()))


with open("articles.json", "r") as f:
    ARTICLES = json.loads(f.read())
ARTICLES_IDS = set((a["gist_id"] for a in ARTICLES))


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__).split('/')[:-1])),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False
)


def setTemplate(self, template_values, templateFile):
    _templateFolder = 'templates/'
    # add Defaults
    template_values['_templateFolder'] = _templateFolder
    template_values['_year'] = str(datetime.datetime.now().year)

    path = os.path.normpath(_templateFolder+templateFile)
    template = JINJA_ENVIRONMENT.get_template(path)
    self.response.write(template.render(template_values))


class MainPage(webapp2.RequestHandler):

    def get(self):
        packages = [
            dict(name="SimPEG", link="simpeg", status="check",
                 color="green",
                 description="A framework for simulation and gradient based parameter estimation in geophysics."),
            dict(name="simpegEM", link="simpeg", status="check",
                 color="green",
                 description="A electromagnetic forward modeling and inversion package for SimPEG."),
            dict(name="simpegNSEM", link="simpeg", status="refresh",
                 color="green",
                 description="Magnetotellurics forward and inverse codes for SimPEG"),
            dict(name="simpegDC", link="simpeg", status="refresh",
                 color="orange",
                 description="A DC resistivity forward modelling and inversion package for SimPEG."),
            dict(name="simpegPF", link="simpeg", status="refresh",
                 color="orange",
                 description="Potential fields codes for SimPEG. Gravity and Magnetics."),
            dict(name="simpegFLOW", link="simpeg", status="flask",
                 color="orange",
                 description="Groundwater (vadose zone) flow equations written in the SimPEG framework."),
            dict(name="simpegSEIS", link="simpegseis", status="wrench",
                 color="grey",
                 description="Time and frequency domain forward modeling and inversion of seismic wave."),
            dict(name="simpegGPR", link="simpeggpr", status="wrench",
                 color="grey",
                 description="Forward modelling and inversion of Ground-Penetrating Radar (GPR)."),
        ]
        setTemplate(self, {"indexPage": True, "packages": packages}, 'index.html')


class Why(webapp2.RequestHandler):
    def get(self):
        setTemplate(self, {}, 'why.html')


baseURL = 'https://www.3ptscience.com'


class Journals(webapp2.RequestHandler):
    def get(self):
        js = ARTICLES
        for i, j in enumerate(js):
            j['index'] = i
        setTemplate(self, {'blogs': js, 'numBlogs': len(js)}, 'journals.html')


def getJournal(uid):
    url = baseURL + "/api/blog/" + uid
    result = urlfetch.fetch(url)
    if not result.status_code == 200:
        return None
    return json.loads(result.content)


class Journal(webapp2.RequestHandler):
    def get(self):
        slug = self.request.path.split('/')[-1]

        if slug not in ARTICLES_IDS:
            setTemplate(self, {}, 'error.html')
            return

        ga = GistArticle(slug)
        setTemplate(self, {'article': ga}, 'article.html')


class Contact(webapp2.RequestHandler):
    def get(self, mailSent=False):
        data = {'mailSent': mailSent}
        setTemplate(self, data, 'contact.html')

    def post(self):
        email = self.request.get('email')
        name = self.request.get('name')
        message = self.request.get('message')

        sender_address = "SimPEG Mail <rowanc1@gmail.com>"
        email_to = "Rowan Cockett <rowanc1@gmail.com>"
        email_subject = "SimPEGMail"
        email_message = "New email from:\n\n%s<%s>\n\n\n%s\n" % (name, email, message)

        mail.send_mail(sender_address, email_to, email_subject, email_message)
        self.get(mailSent=True)


class Images(webapp2.RequestHandler):
    def get(self):
        self.redirect('http://www.3ptscience.com' + self.request.path)


class Error(webapp2.RequestHandler):
    def get(self):
        setTemplate(self, {}, 'error.html')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/journal', Journals),
    ('/journal/', Journals),
    ('/why', Why),
    ('/journal/.*', Journal),
    ('/img/.*', Images),
    ('/contact', Contact),
    ('/.*', Error),
], debug=os.environ.get("SERVER_SOFTWARE", "").startswith("Dev"))
