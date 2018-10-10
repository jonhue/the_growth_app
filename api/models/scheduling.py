import datetime as dt
from mongoengine import *


class Scheduling(EmbeddedDocument):
    DEFAULT_TYPE = ''
    TYPES = [DEFAULT_TYPE, '']

    type = StringField(required=True, default=DEFAULT_TYPE)
    time = DateTimeField(required=True)
    ends_at = DateTimeField()
    ands_after = IntField()
    created_at = DateTimeField(required=True, default=dt.datetime.now())
