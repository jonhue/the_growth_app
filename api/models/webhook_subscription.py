import datetime as dt
import requests
from mongoengine import *

from .user import User
from .client import Client
from .webhook_event import WebhookEvent


class WebhookSubscription(EmbeddedDocument):
    client = ReferenceField(Client, required=True)
    user = ReferenceField(User, required=True)
    url = URLField(required=True)
    event_types = ListField(StringField, required=True, default=WebhookEvent.TYPES)
    events = SortedListField(ReferenceField(WebhookEvent))
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    def send(self, event):
        requests.post(self.url, data={
            'webhook_id': self.id,
            'token': self.client.token,
            'type': event.type,
            'payload': event.payload
        })
