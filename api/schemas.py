from marshmallow import Schema, fields

from .models import *


class UserSchema(Schema):
    private = fields.Boolean()
    notifications = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    class Meta:
        fields = ('username', 'email', 'name', 'avatar', 'private', 'notifications', 'language', 'created_at')
        ordered = True



class CollaborationSchema(Schema):
    id = fields.String(dump_only=True)
    inviter = fields.Nested(UserSchema)
    invited = fields.Nested(UserSchema)
    state = fields.String(dump_only=True)
    position = fields.Integer()
    notifications = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    class Meta:
        fields = ('id', 'inviter', 'invited', 'state', 'position', 'notifications', 'created_at')
        ordered = True


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
