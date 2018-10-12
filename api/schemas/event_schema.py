from marshmallow import Schema, fields

from .fields import Fields


class EventSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested('UserSchema', only=Fields.User.compact)
    growthbook = fields.Nested('GrowthbookSchema', only=Fields.Growthbook.compact)
    datetime = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = Fields.Event.default
        ordered = True
