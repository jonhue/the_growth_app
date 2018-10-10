import datetime as dt
from mongoengine import *


class LogAttachment(EmbeddedDocument):
    url = URLField(required=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())
