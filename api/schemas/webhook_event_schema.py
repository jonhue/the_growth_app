from marshmallow import Schema, fields

from .user_schema import UserSchema


class WebhookEventSchema(Schema):
    id = fields.String(dump_only=True)
    users = fields.Nested(UserSchema, many=True, only=UserSchema.Meta.COMPACT_FIELDS, dump_only=True)
    type = fields.String(dump_only=True)
    payload = fields.Dict(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        DEFAULT_FIELDS = ('id', 'users', 'type', 'payload', 'created_at')
        COMPACT_FIELDS = ('id', 'type')

        fields = DEFAULT_FIELDS
        ordered = True
