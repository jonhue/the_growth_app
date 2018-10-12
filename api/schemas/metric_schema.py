from marshmallow import Schema, fields

from .fields import Fields


class MetricSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested('UserSchema', only=Fields.User.compact)
    growthbook = fields.Nested('GrowthbookSchema', only=Fields.Growthbook.compact)
    item = fields.Dict(dump_only=True)
    attributes = fields.List(fields.String())
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = Fields.Metric.default
        ordered = True
