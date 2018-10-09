import datetime as dt
from mongoengine import *
from passlib.hash import pbkdf2_sha256 as sha256
from transitions import Machine



class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    name = StringField(required=True)
    password = StringField(required=True)
    avatar = URLField()
    private = BooleanField(required=True, default=True)
    notifications = BooleanField(required=True, default=False)
    language = StringField(required=True, default='en')
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)



class Collaboration(EmbeddedDocument):
    INITIAL_STATE = 'proposed'
    STATES = [INITIAL_STATE, 'accepted']

    inviter = ReferenceField(User)
    invited = ReferenceField(User)
    state = StringField(required=True, default=INITIAL_STATE)
    position = IntField(required=True)
    notifications = BooleanField(required=True, default=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)

        self.machine = Machine(model=self, states=Collaboration.STATES, initial=Collaboration.INITIAL_STATE)
        self.macine.add_transition('accept', 'proposed', 'accepted')


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



class Scheduling(EmbeddedDocument):
    DEFAULT_TYPE = ''
    TYPES = [DEFAULT_TYPE, '']

    type = StringField(required=True, default=DEFAULT_TYPE)
    time = DateTimeField(required=True)
    ends_at = DateTimeField()
    ands_after = IntField()
    created_at = DateTimeField(required=True, default=dt.datetime.now())


class Event(EmbeddedDocument):
    datetime = DateTimeField(required=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())


class LogAttachment(EmbeddedDocument):
    url = URLField(required=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())


class Log(EmbeddedDocument):
    user = ReferenceField(User, required=True)
    content = StringField()
    attachment = EmbeddedDocumentField(LogAttachment)
    created_at = DateTimeField(required=True, default=dt.datetime.now())


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

    meta = {'allow_inheritance': True}

    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)

        self.machine = Machine(model=self, states=Task.STATES, initial=Task.INITIAL_STATE)
        self.machine.add_transition('complete', 'active', 'done')


class Goal(Task):
    logs = SortedListField(EmbeddedDocumentField(Log))
    name = StringField(required=True)


class ActionItem(Task):
    parent = GenericReferenceField(required=True)
    title = StringField(required=True)



class Metric(Document):
    DEFAULT_TYPE = ''
    TYPES = [DEFAULT_TYPE, '']
    DEFAULT_INTERVAL = 'monthly'
    INTERVALS = ['weekly', DEFAULT_INTERVAL, 'yearly']

    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    growthbook = ReferenceField(Growthbook, reverse_delete_rule=CASCADE, required=True)
    item = GenericReferenceField(required=True)
    type = StringField(required=True, default=DEFAULT_TYPE)
    interval = StringField(required=True, default=DEFAULT_INTERVAL)
    attributes = SortedListField(StringField())
    created_at = DateTimeField(required=True, default=dt.datetime.now())
