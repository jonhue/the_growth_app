import datetime as dt
from mongoengine import *
from transitions import Machine

from .user import User


class Collaboration(EmbeddedDocument):
    INITIAL_STATE = 'proposed'
    STATES = [INITIAL_STATE, 'accepted']

    inviter = ReferenceField(User, required=True)
    invited = ReferenceField(User, required=True)
    state = StringField(required=True, default=INITIAL_STATE)
    position = IntField(required=True)
    notifications = BooleanField(required=True, default=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)

        self.machine = Machine(model=self, states=Collaboration.STATES, initial=Collaboration.INITIAL_STATE)
        self.macine.add_transition('accept', 'proposed', 'accepted')
