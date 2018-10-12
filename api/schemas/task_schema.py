from marshmallow import Schema, fields

from .fields import Fields


class TaskSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested('UserSchema', only=Fields.User.compact)
    growthbook = fields.Nested('GrowthbookSchema', only=Fields.Growthbook.compact)
    scheduling = fields.Nested('SchedulingSchema', only=Fields.Scheduling.compact)
    events = fields.Nested('EventSchema', many=True, only=Fields.Event.compact)
    state = fields.String(dump_only=True)
    position = fields.Integer()
    created_at = fields.DateTime(dump_only=True)
