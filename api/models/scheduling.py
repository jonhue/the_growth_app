import datetime as dt
from mongoengine import *

from .user import User


class Scheduling(EmbeddedDocument):
    DEFAULT_TYPE = 'daily'
    TYPES = (DEFAULT_TYPE, 'weekdays', 'weekends', 'weekly', 'monthly')

    user = ReferenceField(User, required=True)
    type = StringField(required=True, default=DEFAULT_TYPE, choices=TYPES)
    time = DateTimeField(required=True)
    ends_at = DateTimeField()
    ands_after = IntField()
    created_at = DateTimeField(required=True, default=dt.datetime.now())
