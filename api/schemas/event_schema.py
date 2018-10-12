from marshmallow import Schema, fields

from .fields import Fields


class EventSchema(Schema):
    id = fields.String(dump_only=True)
    datetime = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = Fields.Event.default
        ordered = True
