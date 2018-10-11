import datetime as dt
from mongoengine import *
from transitions import Machine

from .user import User
from .growthbook import Growthbook
from .scheduling import Scheduling
from .event import Event


class Task(Document):
    INITIAL_STATE = 'active'
    STATES = [INITIAL_STATE, 'done']

    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    growthbook = ReferenceField(Growthbook, reverse_delete_rule=CASCADE, required=True)
    scheduling = EmbeddedDocumentField(Scheduling)
    events = SortedListField(EmbeddedDocumentField(Event))
    state = StringField(required=True, default=INITIAL_STATE)
    position = IntField(required=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    meta = {'abstract': True}

    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)

        self.machine = Machine(model=self, states=Task.STATES, initial=Task.INITIAL_STATE)
        self.machine.add_transition('complete', 'active', 'done')
