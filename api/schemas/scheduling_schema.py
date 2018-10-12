from marshmallow import Schema, fields

from .fields import Fields


class SchedulingSchema(Schema):
    id = fields.String(dump_only=True)
    time = fields.DateTime()
    ends_at = fields.DateTime()
    ends_after = fields.Integer()
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = Fields.Scheduling.default
        ordered = True
