import datetime as dt
from mongoengine import *

from .user import User
from .growthbook import Growthbook


class Event(EmbeddedDocument):
    user = ReferenceField(User, required=True)
    growthbook = ReferenceField(Growthbook, required=True)
    datetime = DateTimeField(required=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())
