from google.appengine.ext import ndb


class Message(ndb.Model):
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()
    subject = ndb.StringProperty()
    message = ndb.TextProperty()
    status = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now=True)
