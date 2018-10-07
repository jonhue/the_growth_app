from marshmallow import Schema, fields

from .models import *


class UserSchema(Schema):
    created_at = fields.String(dump_only=True)
    class Meta:
        fields = ('username', 'email', 'name', 'avatar', 'private', 'notifications', 'language', 'created_at')
        ordered = True
