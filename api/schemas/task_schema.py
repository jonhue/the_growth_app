from marshmallow import Schema, fields

from .user_schema import UserSchema
from .growthbook_schema import GrowthbookSchema
from .scheduling_schema import SchedulingSchema
from .event_schema import EventSchema


class TaskSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, only=UserSchema.Meta.COMPACT_FIELDS)
    growthbook = fields.Nested(GrowthbookSchema, only=GrowthbookSchema.Meta.COMPACT_FIELDS)
    scheduling = fields.Nested(SchedulingSchema, only=SchedulingSchema.Meta.COMPACT_FIELDS)
    events = fields.Nested(EventSchema, many=True, only=EventSchema.Meta.COMPACT_FIELDS)
    state = fields.String(dump_only=True)
    position = fields.Integer()
    created_at = fields.DateTime(dump_only=True)
