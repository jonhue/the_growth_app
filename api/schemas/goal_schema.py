from marshmallow import fields

from .task_schema import TaskSchema

from .fields import Fields


class GoalSchema(TaskSchema):
    logs = fields.Nested('LogSchema', many=True, only=Fields.Log.compact)

    class Meta:
        fields = Fields.Goal.default
        ordered = True
