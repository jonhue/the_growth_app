import datetime as dt
import os, binascii
from mongoengine import *

from .user import User
from .webhook_subscription import WebhookSubscription


class Client(Document):
    name = StringField(required=True)
    user = ReferenceField(User, required=True)
    subscriptions = ListField(EmbeddedDocumentField(WebhookSubscription))
    token = StringField(required=True, default=binascii.b2a_hex(os.urandom(15)))
    created_at = DateTimeField(required=True, default=dt.datetime.now())
