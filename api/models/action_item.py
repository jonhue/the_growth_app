import datetime as dt
from mongoengine import *

from .task import Task
from .goal import Goal


class ActionItem(Task):
    parent = ReferenceField('self', reverse_delete_rule=CASCADE)
    goal = ReferenceField(Goal, reverse_delete_rule=CASCADE)
    title = StringField(required=True)
