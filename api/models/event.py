import datetime as dt
from mongoengine import *

from .user import User


class Event(EmbeddedDocument):
    user = ReferenceField(User, required=True)
    datetime = DateTimeField(required=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())
