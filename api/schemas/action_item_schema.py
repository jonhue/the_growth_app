from marshmallow import fields

from .task_schema import TaskSchema
from .goal_schema import GoalSchema


class ActionItemSchema(TaskSchema):
    parent = fields.Nested('self', only=fields('compact'))
    goal = fields.Nested(GoalSchema, only=GoalSchema.Meta.COMPACT_FIELDS)

    class Meta:
        DEFAULT_FIELDS = ('id', 'user', 'growthbook', 'scheduling', 'events', 'parent', 'goal', 'title', 'state', 'position', 'created_at')
        COMPACT_FIELDS = ('id', 'title', 'state')

        fields = DEFAULT_FIELDS
        ordered = True
