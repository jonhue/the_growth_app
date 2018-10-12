from marshmallow import Schema, fields

from .fields import Fields


class LogSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested('UserSchema', only=Fields.User.compact)
    attachments = fields.Nested('LogAttachmentSchema', many=True, only=Fields.LogAttachment.compact)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = Fields.Log.default
        ordered = True
