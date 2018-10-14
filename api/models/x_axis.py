from mongoengine import *


class XAxis(EmbeddedDocument):
    DEFAULT_INTERVAL = 'weekly'
    INTERVALS = ('daily', DEFAULT_INTERVAL, 'monthly', 'yearly')

    interval = StringField(required=True, default=DEFAULT_INTERVAL, choices=INTERVALS)
    length = IntField(required=True, default=4)
    ends_at = DateTimeField()
