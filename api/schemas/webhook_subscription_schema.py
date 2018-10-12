from marshmallow import Schema, fields

from .fields import Fields


class WebhookSubscriptionSchema(Schema):
    id = fields.String(dump_only=True)
    client = fields.Nested('ClientSchema', only=Fields.Client.compact)
    user = fields.Nested('UserSchema', only=Fields.User.compact)
    # event_types
    events = fields.Nested('WebhookEventSchema', many=True, only=Fields.WebhookEvent.compact)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = Fields.WebhookSubscription.default
        ordered = True
