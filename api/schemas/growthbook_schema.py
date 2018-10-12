from marshmallow import Schema, fields

from .fields import Fields


class GrowthbookSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested('UserSchema', only=Fields.User.compact)
    collaborations = fields.Nested('CollaborationSchema', many=True, only=Fields.Collaboration.compact, dump_only=True)
    state = fields.String(dump_only=True)
    position = fields.Integer()
    notifications = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = Fields.Growthbook.default
        ordered = True
