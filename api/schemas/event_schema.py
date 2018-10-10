from marshmallow import Schema, fields


class EventSchema(Schema):
    id = fields.String(dump_only=True)
    datetime = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        DEFAULT_FIELDS = ('id', 'datetime', 'created_at')
        COMPACT_FIELDS = ('id', 'datetime')

        fields = DEFAULT_FIELDS
        ordered = True
