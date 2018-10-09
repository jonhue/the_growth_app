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
    inviter = ReferenceField(User)
    invited = ReferenceField(User)
    state = StringField(required=True, default='proposed')
    position = IntField(required=True)
    notifications = BooleanField(required=True, default=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    states = ['proposed', 'accepted']

    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)

        self.machine = Machine(model=self, states=Collaboration.states)
        self.macine.add_transition('accept', 'proposed', 'accepted')


class Growthbook(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    collaborations = ListField(EmbeddedDocumentField(Collaboration))
    state = StringField(required=True, default='active')
    name = StringField(required=True)
    position = IntField(required=True)
    notifications = BooleanField(required=True, default=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    states = ['active', 'archived']

    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)

        self.machine = Machine(model=self, states=Growthbook.states)
        self.machine.add_transition('archive', 'active', 'archived')



class Scheduling(EmbeddedDocument):
    type = StringField(required=True, default='')
    time = DateTimeField(required=True)
    ends_at = DateTimeField()
    ands_after = IntField()
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    types = ['']


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
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    growthbook = ReferenceField(Growthbook, reverse_delete_rule=CASCADE, required=True)
    scheduling = EmbeddedDocumentField(Scheduling)
    events = SortedListField(EmbeddedDocumentField(Event))
    state = StringField(required=True, default='active')
    position = IntField(required=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    states = ['active', 'done']
    meta = {'allow_inheritance': True}

    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)

        self.machine = Machine(model=self, states=Task.states)
        self.machine.add_transition('complete', 'active', 'done')


class Goal(Task):
    logs = SortedListField(EmbeddedDocumentField(Log))
    name = StringField(required=True)


class ActionItem(Task):
    parent = GenericReferenceField(required=True)
    title = StringField(required=True)



class Metric(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    growthbook = ReferenceField(Growthbook, reverse_delete_rule=CASCADE, required=True)
    item = GenericReferenceField(required=True)
    type = StringField(required=True, default='')
    interval = StringField(required=True, default='monthly')
    attributes = SortedListField(StringField())
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    types = ['']
    intervals = ['weekly', 'monthly', 'yearly']
