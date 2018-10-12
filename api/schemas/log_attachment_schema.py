from marshmallow import Schema, fields

from .fields import Fields


class LogAttachmentSchema(Schema):
    id = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = Fields.LogAttachment.default
        ordered = True
