import datetime as dt
from mongoengine import *

from .task import Task
from .log import Log


class Goal(Task):
    logs = SortedListField(EmbeddedDocumentField(Log))
    name = StringField(required=True)
