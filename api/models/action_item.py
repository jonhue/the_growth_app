import datetime as dt
from mongoengine import *

from .goal import Goal
from .task import Task


class ActionItem(Task):
    parent = ReferenceField('self', reverse_delete_rule=CASCADE)
    goal = ReferenceField(Goal, reverse_delete_rule=CASCADE)
    title = StringField(required=True)
