import datetime as dt
from mongoengine import *


class Event(EmbeddedDocument):
    datetime = DateTimeField(required=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())
