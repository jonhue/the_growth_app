import datetime as dt
from mongoengine import *
from transitions import Machine

from .user import User
from .collaboration import Collaboration


class Growthbook(Document):
    INITIAL_STATE = 'active'
    STATES = [INITIAL_STATE, 'archived']

    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    collaborations = ListField(EmbeddedDocumentField(Collaboration))
    state = StringField(required=True, default=INITIAL_STATE)
    name = StringField(required=True)
    position = IntField(required=True)
    notifications = BooleanField(required=True, default=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)

        self.machine = Machine(model=self, states=Growthbook.STATES, initial=Growthbook.INITIAL_STATE)
        self.machine.add_transition('archive', 'active', 'archived')
