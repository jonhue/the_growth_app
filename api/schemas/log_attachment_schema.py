from marshmallow import Schema, fields


class LogAttachmentSchema(Schema):
    id = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        DEFAULT_FIELDS = ('id', 'url', 'created_at')
        COMPACT_FIELDS = ('id', 'url')

        fields = DEFAULT_FIELDS
        ordered = True
