from marshmallow import fields

from .task_schema import TaskSchema

from .fields import Fields


class ActionItemSchema(TaskSchema):
    parent = fields.Nested('self', only=(Fields.ActionItem.compact))
    goal = fields.Nested('GoalSchema', only=Fields.Goal.compact)

    class Meta:
        fields = Fields.ActionItem.default
        ordered = True
