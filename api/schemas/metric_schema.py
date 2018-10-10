from marshmallow import Schema, fields

from .user_schema import UserSchema
from .growthbook_schema import GrowthbookSchema


class MetricSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, only=UserSchema.Meta.COMPACT_FIELDS)
    growthbook = fields.Nested(GrowthbookSchema, only=GrowthbookSchema.Meta.COMPACT_FIELDS)
    # item
    # attributes
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        DEFAULT_FIELDS = ('id', 'user', 'growthbook', 'item', 'type', 'interval', 'attributes', 'created_at')
        COMPACT_FIELDS = ('id', 'item', 'type', 'interval', 'attributes')

        fields = DEFAULT_FIELDS
        ordered = True
