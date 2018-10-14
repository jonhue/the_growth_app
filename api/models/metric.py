import datetime as dt
from mongoengine import *

from .entity import Entity
from .growthbook import Growthbook
from .user import User
from .x_axis import XAxis
from .y_axis import YAxis


class Metric(Document):
    DEFAULT_TYPE = 'line'
    TYPES = (DEFAULT_TYPE, 'bar', 'pie', 'radar')
    DEFAULT_STYLE = 'vertical'
    STYLES = (DEFAULT_STYLE, 'horizontal', 'stacked')

    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    growthbook = ReferenceField(Growthbook, reverse_delete_rule=CASCADE, required=True)
    item = GenericReferenceField()
    entities = ListField(EmbeddedDocumentField(Entity))
    type = StringField(required=True, default=DEFAULT_TYPE, choices=TYPES)
    style = StringField(required=True, default=DEFAULT_STYLE, choices=STYLES)
    y_axis = EmbeddedDocumentField(YAxis)
    x_axis = EmbeddedDocumentField(XAxis)
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    def clean(self):
        if self.y_axis is None:
            if self.type == 'line' or self.type == 'bar' or self.type == 'radar':
                raise ValidationError(self.type + 'requires a y-axis')
        if self.x_axis is None:
            if self.type == 'line' or self.type == 'radar':
                raise ValidationError(self.type + 'requires an x-axis')
