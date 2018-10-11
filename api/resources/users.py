from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from ..models import User
from ..schemas import UserSchema

from .responses import respond


class UserListResource(Resource):
    @jwt_required
    def get(self):
        schema = UserSchema(many=True, only=UserSchema.Meta.COMPACT_FIELDS)
        users = User.objects(private=False)

        return respond(200, {'users': schema.dump(users).data})


class UserResource(Resource):
    @jwt_required
    def get(self, username):
        try:
            user = User.objects.get(username=username)
        except DoesNotExist:
            return respond(404, {}, ['User does not exist'])

        if get_jwt_identity() == user.username:
            schema = UserSchema()
        else:
            if user.private is True:
                return respond(403, {}, ['Access forbidden'])
            else:
                schema = UserSchema(only=UserSchema.Meta.COMPACT_FIELDS)

        return respond(200, {'user': schema.dump(user).data})

    @jwt_required
    def put(self, username):
        try:
            user = User.objects.get(username=username)
        except DoesNotExist:
            return respond(404, {}, ['User does not exist'])

        if get_jwt_identity() == user.username:
            schema = UserSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        try:
            user.update(**schema.load(request.args).data)
            # Return updated document
            user = User.objects.get(username=username)
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(200, {'user': schema.dump(user).data})

    @jwt_required
    def delete(self, username):
        try:
            user = User.objects.get(username=username)
        except DoesNotExist:
            return respond(404, {}, ['User does not exist'])

        if get_jwt_identity() != user.username:
            return respond(403, {}, ['Access forbidden'])

        user.delete()
        return respond(204)
