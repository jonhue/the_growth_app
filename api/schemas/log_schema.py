from marshmallow import Schema, fields

from .user_schema import UserSchema
from .log_attachment_schema import LogAttachmentSchema


class LogSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, only=UserSchema.Meta.COMPACT_FIELDS)
    attachments = fields.Nested(LogAttachmentSchema, many=True, only=LogAttachmentSchema.Meta.COMPACT_FIELDS)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        DEFAULT_FIELDS = ('id', 'user', 'content', 'attachments', 'created_at')
        COMPACT_FIELDS = ('id', 'content', 'attachments')

        fields = DEFAULT_FIELDS
        ordered = True
