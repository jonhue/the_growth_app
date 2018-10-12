import datetime as dt
from mongoengine import *

from .log_attachment import LogAttachment
from .user import User


class Log(EmbeddedDocument):
    user = ReferenceField(User, required=True)
    content = StringField()
    attachments = SortedListField(EmbeddedDocumentField(LogAttachment))
    created_at = DateTimeField(required=True, default=dt.datetime.now())
