from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_refresh_token_required, jwt_required
from flask_restful import Resource

from .models import *
from .schemas import *


def respond(code=200, payload={}, messages=[]):
    return {
        'status': 'ok' if int(code/100) == 2 else 'error',
        'code': code,
        'messages': messages,
        'payload': payload,
    }, code



class UserListResource(Resource):
    @jwt_required
    def get(self):
        schema = UserSchema(many=True, only=('username', 'name', 'avatar'))
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
                schema = UserSchema(only=('username', 'name', 'avatar'))

        return respond(200, {'user': schema.dump(user).data})

    @jwt_required
    def put(self, username):
        schema = UserSchema()

        try:
            user = User.objects.get(username=username)
        except DoesNotExist:
            return respond(404, {}, ['User does not exist'])

        if get_jwt_identity() != user.username:
            return respond(403, {}, ['Access forbidden'])

        try:
            user.update(**schema.load(request.args).data)
            # Return updated document
            user = User.objects.get(username=username)
        except NotUniqueError as e:
            return respond(400, {}, ['Uniqueness error', str(e)])
        except ValidationError as e:
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


class UserRegistrationResource(Resource):
    def post(self):
        schema = UserSchema()
        user = User(**schema.load(request.args).data)
        user.password = User.generate_hash(request.args['password'])

        try:
            user.save()
        except NotUniqueError as e:
            return respond(400, {}, ['Uniqueness error', str(e)])
        except ValidationError as e:
            return respond(400, {}, ['Validation error', str(e)])

        access_token = create_access_token(identity=request.args['username'])
        refresh_token = create_refresh_token(identity=request.args['username'])

        return respond(201, {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': schema.dump(user).data,
        })


class UserLoginResource(Resource):
    def post(self):
        schema = UserSchema()

        try:
            user = User.objects.get(username=request.args['username'])
        except DoesNotExist:
            return respond(404, {}, ['User does not exist'])

        if User.verify_hash(request.args['password'], user.password):
            access_token = create_access_token(identity=request.args['username'])
            refresh_token = create_refresh_token(identity=request.args['username'])
            return respond(200, {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': schema.dump(user).data,
            })
        else:
            return respond(400, {}, ['Wrong credentials'])


class RefreshTokenResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        username = get_jwt_identity()
        access_token = create_access_token(identity=username)
        return respond(200, {'access_token': access_token})



class GrowthbookListResource(Resource):
    @jwt_required
    def post(self):
        schema = GrowthbookSchema()
        growthbook = Growthbook(**schema.load(request.args).data)
        growthbook.user = User.objects.get(username=request.args['user'])

        try:
            growthbook.save()
        except NotUniqueError as e:
            return respond(400, {}, ['Uniqueness error', str(e)])
        except ValidationError as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(201, {'growthbook': schema.dump(growthbook).data})


class GrowthbookResource(Resource):
    @jwt_required
    def get(self, id):
        try:
            growthbook = Growthbook.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Growthbook does not exist'])

        if get_jwt_identity() == growthbook.user.username:
            schema = GrowthbookSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        return respond(200, {'growthbook': schema.dump(growthbook).data})

    @jwt_required
    def put(self, id):
        schema = GrowthbookSchema()

        try:
            growthbook = Growthbook.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Growthbook does not exist'])

        if get_jwt_identity() != growthbook.user.username:
            return respond(403, {}, ['Access forbidden'])

        try:
            growthbook.update(**schema.load(request.args).data)
            # Return updated document
            growthbook = Growthbook.objects.get(id=id)
        except NotUniqueError as e:
            return respond(400, {}, ['Uniqueness error', str(e)])
        except ValidationError as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(200, {'growthbook': schema.dump(growthbook).data})

    @jwt_required
    def delete(self, id):
        try:
            growthbook = Growthbook.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Growthbook does not exist'])

        if get_jwt_identity() != growthbook.user.username:
            return respond(403, {}, ['Access forbidden'])

        growthbook.delete()
        return respond(204)
