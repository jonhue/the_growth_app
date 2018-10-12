from marshmallow import Schema, fields

from .fields import Fields


class WebhookEventSchema(Schema):
    id = fields.String(dump_only=True)
    users = fields.Nested('UserSchema', many=True, only=Fields.User.compact, dump_only=True)
    type = fields.String(dump_only=True)
    payload = fields.Dict(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = Fields.WebhookEvent.default
        ordered = True
