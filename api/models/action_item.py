import datetime as dt
from mongoengine import *

from .task import Task


class ActionItem(Task):
    parent = GenericReferenceField(required=True)
    title = StringField(required=True)
