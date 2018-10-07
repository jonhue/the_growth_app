from marshmallow import Schema, fields, post_load

from .models import *


class UserSchema(Schema):
    created_at = fields.String(dump_only=True)
    class Meta:
        fields = ('username', 'email', 'name', 'avatar', 'private', 'notifications', 'language', 'created_at')
        ordered = True

    @post_load
    def make_user(self, data):
        return User(**data)
