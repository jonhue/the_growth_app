from marshmallow import Schema, fields

from .fields import Fields


class YAxisSchema(Schema):
    id = fields.String(dump_only=True)
    max = fields.Int()
    min = fields.Int()

    class Meta:
        fields = Fields.YAxis.default
        ordered = True
