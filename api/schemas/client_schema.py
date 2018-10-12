from marshmallow import Schema, fields

from .fields import Fields


class ClientSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested('UserSchema', only=Fields.User.compact)
    subscriptions = fields.Nested('WebhookSubscriptionSchema', many=True, only=Fields.WebhookSubscription.compact)
    token = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = Fields.Client.default
        ordered = True
