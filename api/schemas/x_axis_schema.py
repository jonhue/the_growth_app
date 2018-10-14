from marshmallow import Schema, fields

from .fields import Fields


class XAxisSchema(Schema):
    id = fields.String(dump_only=True)
    length = fields.Int()
    ends_at = fields.DateTime()

    class Meta:
        fields = Fields.XAxis.default
        ordered = True
