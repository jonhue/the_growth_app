import datetime as dt
from mongoengine import *

from .log import Log
from .task import Task


class Goal(Task):
    logs = SortedListField(EmbeddedDocumentField(Log))
    name = StringField(required=True)
