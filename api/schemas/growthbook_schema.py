from marshmallow import Schema, fields

from .user_schema import UserSchema
from .collaboration_schema import CollaborationSchema


class GrowthbookSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, only=UserSchema.Meta.COMPACT_FIELDS)
    collaborations = fields.Nested(CollaborationSchema, many=True, only=CollaborationSchema.Meta.COMPACT_FIELDS, dump_only=True)
    state = fields.String(dump_only=True)
    position = fields.Integer()
    notifications = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        DEFAULT_FIELDS = ('id', 'user', 'collaborations', 'state', 'name', 'position', 'notifications', 'created_at')
        COMPACT_FIELDS = ('id', 'state', 'name')

        fields = DEFAULT_FIELDS
        ordered = True
