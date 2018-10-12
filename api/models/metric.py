import datetime as dt
from mongoengine import *

from .growthbook import Growthbook
from .user import User


class Metric(Document):
    DEFAULT_TYPE = ''
    TYPES = [DEFAULT_TYPE, '']
    DEFAULT_INTERVAL = 'monthly'
    INTERVALS = ['weekly', DEFAULT_INTERVAL, 'yearly']

    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    growthbook = ReferenceField(Growthbook, reverse_delete_rule=CASCADE, required=True)
    item = GenericReferenceField()
    type = StringField(required=True, default=DEFAULT_TYPE)
    interval = StringField(required=True, default=DEFAULT_INTERVAL)
    attributes = SortedListField(StringField())
    created_at = DateTimeField(required=True, default=dt.datetime.now())
