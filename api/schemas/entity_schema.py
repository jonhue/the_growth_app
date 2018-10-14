from marshmallow import Schema, fields

from .fields import Fields


class EntitySchema(Schema):
    id = fields.String(dump_only=True)
    datapoints = fields.List(fields.String())

    class Meta:
        fields = Fields.Entity.default
        ordered = True
