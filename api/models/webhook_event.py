import datetime as dt
from mongoengine import *

from .user import User
from .webhook_subscription import WebhookSubscription


class WebhookEvent(Document):
    users = ListField(ReferenceField(User))
    type = StringField(required=True)
    payload = DictField(required=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    def save(self):
        super().save()
        self.push()

    def push(self):
        for user in self.users:
            webhooks = WebhookSubscription.objects.get(user=user)
            for webhook in webhooks:
                if self.type in webhook.event_types:
                    webhook.send(self)
