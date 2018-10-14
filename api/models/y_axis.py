from mongoengine import *


class YAxis(EmbeddedDocument):
    DEFAULT_SCALE = 'linear'
    SCALES = (DEFAULT_SCALE, 'logarithmic')

    scale = StringField(required=True, default=DEFAULT_SCALE, choices=SCALES)
    max = IntField()
    min = IntField()
