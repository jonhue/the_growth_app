from marshmallow import Schema, fields

from .fields import Fields


class CollaborationSchema(Schema):
    id = fields.String(dump_only=True)
    inviter = fields.Nested('UserSchema')
    invited = fields.Nested('UserSchema')
    state = fields.String(dump_only=True)
    position = fields.Integer()
    notifications = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = Fields.Collaboration.default
        ordered = True
