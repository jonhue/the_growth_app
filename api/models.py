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


class Growthbook(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    state = StringField(required=True, default='active')
    name = StringField(required=True)
    position = IntField(required=True)
    notifications = BooleanField(required=True, default=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    states = ['active', 'archived']

    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)

        self.machine = Machine(model=self, states=Growthbook.states, initial='active')
        self.machine.add_transition('archive', 'active', 'archived')


class Goal(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    growthbook = ReferenceField(Growthbook, reverse_delete_rule=CASCADE)
    state = StringField(required=True, default='active')
    name = StringField(required=True)
    position = IntField(required=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    states = ['active', 'done']

    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)

        self.machine = Machine(model=self, states=Goal.states, initial='active')
        self.machine.add_transition('complete', 'active', 'done')


class Task(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    growthbook = ReferenceField(Growthbook, reverse_delete_rule=CASCADE)
    parent = GenericReferenceField(reverse_delete_rule=CASCADE)
    state = StringField(required=True, default='active')
    title = StringField(required=True)
    position = IntField(required=True)
    created_at = DateTimeField(required=True, default=dt.datetime.now())


class Metric(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    growthbook = ReferenceField(Growthbook, reverse_delete_rule=CASCADE)
    item = GenericReferenceField(reverse_delete_rule=CASCADE)
    type = StringField(required=True, default='')
    interval = StringField(required=True, default='monthly')
    attributes = SortedListField(StringField())
    created_at = DateTimeField(required=True, default=dt.datetime.now())

    types = ['']
    intervals = ['weekly', 'monthly', 'yearly']
