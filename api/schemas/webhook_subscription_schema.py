from marshmallow import Schema, fields

from .user_schema import UserSchema
from .client_schema import ClientSchema
from .webhook_event_schema import WebhookEventSchema


class WebhookSubscriptionSchema(Schema):
    id = fields.String(dump_only=True)
    client = fields.Nested(ClientSchema, only=ClientSchema.Meta.COMPACT_FIELDS)
    user = fields.Nested(UserSchema, only=UserSchema.Meta.COMPACT_FIELDS)
    # event_types
    events = fields.Nested(WebhookEventSchema, many=True, only=WebhookEventSchema.Meta.COMPACT_FIELDS)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        DEFAULT_FIELDS = ('id', 'client', 'user', 'url', 'event_types', 'events', 'created_at')
        COMPACT_FIELDS = ('id', 'url', 'event_types')

        fields = DEFAULT_FIELDS
        ordered = True
