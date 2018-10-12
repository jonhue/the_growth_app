from marshmallow import Schema, fields

from .fields import Fields


class UserSchema(Schema):
    private = fields.Boolean()
    notifications = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)

    class Meta(object):
        fields = Fields.User.default
        ordered = True
