from marshmallow import fields

from .task_schema import TaskSchema
from .log_schema import LogSchema


class GoalSchema(TaskSchema):
    logs = fields.Nested(LogSchema, many=True, only=LogSchema.Meta.COMPACT_FIELDS)

    class Meta:
        DEFAULT_FIELDS = ('id', 'user', 'growthbook', 'scheduling', 'events', 'logs', 'name', 'state', 'position', 'created_at')
        COMPACT_FIELDS = ('id', 'name', 'state')

        fields = DEFAULT_FIELDS
        ordered = True
