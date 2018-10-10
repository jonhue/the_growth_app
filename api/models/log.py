import datetime as dt
from mongoengine import *

from .user import User
from .log_attachment import LogAttachment


class Log(EmbeddedDocument):
    user = ReferenceField(User, required=True)
    content = StringField()
    attachments = SortedListField(EmbeddedDocumentField(LogAttachment))
    created_at = DateTimeField(required=True, default=dt.datetime.now())
