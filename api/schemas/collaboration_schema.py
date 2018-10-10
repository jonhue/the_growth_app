from marshmallow import Schema, fields

from .user_schema import UserSchema


class CollaborationSchema(Schema):
    id = fields.String(dump_only=True)
    inviter = fields.Nested(UserSchema)
    invited = fields.Nested(UserSchema)
    state = fields.String(dump_only=True)
    position = fields.Integer()
    notifications = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        DEFAULT_FIELDS = ('id', 'inviter', 'invited', 'state', 'position', 'notifications', 'created_at')
        COMPACT_FIELDS = ('id', 'inviter', 'invited', 'state', 'created_at')

        fields = DEFAULT_FIELDS
        ordered = True
