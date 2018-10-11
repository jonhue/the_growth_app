from marshmallow import Schema, fields

from .user_schema import UserSchema
from .webhook_subscription_schema import WebhookSubscriptionSchema


class ClientSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, only=UserSchema.Meta.COMPACT_FIELDS)
    subscriptions = fields.Nested(WebhookSubscriptionSchema, many=True, only=WebhookSubscriptionSchema.Meta.COMPACT_FIELDS)
    token = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        DEFAULT_FIELDS = ('id', 'name', 'user', 'subscriptions', 'token', 'created_at')
        COMPACT_FIELDS = ('id', 'name')

        fields = DEFAULT_FIELDS
        ordered = True
