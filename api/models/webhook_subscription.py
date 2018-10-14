import datetime as dt
import requests
from mongoengine import *

from .client import Client
from .user import User


class WebhookSubscription(Document):
    EVENT_TYPES = ('event.created')

    client = ReferenceField(Client, reverse_delete_rule=CASCADE, required=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    url = URLField(required=True)
    event_types = ListField(StringField, required=True, default=EVENT_TYPES)
    events = SortedListField(ReferenceField('WebhookEvent'))
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    def send(self, event):
        requests.post(self.url, data={
            'webhook_id': self.id,
            'token': self.client.token,
            'type': event.type,
            'payload': event.payload
        })
