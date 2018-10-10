from marshmallow import Schema, fields


class SchedulingSchema(Schema):
    id = fields.String(dump_only=True)
    time = fields.DateTime()
    ends_at = fields.DateTime()
    ends_after = fields.Integer()
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        DEFAULT_FIELDS = ('id', 'type', 'time', 'ends_at', 'ends_after', 'created_at')
        COMPACT_FIELDS = ('id', 'type', 'time', 'ends_at', 'ends_after')

        fields = DEFAULT_FIELDS
        ordered = True
