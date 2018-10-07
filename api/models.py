import datetime as dt
from mongoengine import *
from passlib.hash import pbkdf2_sha256 as sha256


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
