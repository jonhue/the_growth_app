from marshmallow import Schema, fields

from .users import UserSchema
from .collaborations import CollaborationSchema


class GrowthbookSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, only=('username', 'name', 'avatar'))
    collaborations = fields.Nested(CollaborationSchema, many=True, only=('id', 'inviter', 'invited', 'state', 'created_at'), dump_only=True)
    state = fields.String(dump_only=True)
    position = fields.Integer()
    notifications = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    class Meta:
        fields = ('id', 'user', 'collaborations', 'state', 'name', 'position', 'notifications', 'created_at')
        ordered = True
