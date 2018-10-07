from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_refresh_token_required, jwt_required
from flask_restful import Resource

from .models import *
from .schemas import *


class UserListResource(Resource):
    @jwt_required
    def get(self):
        schema = UserSchema(many=True)
        users = User.objects(private=False)

        return schema.dump(users).data, 200


class UserResource(Resource):
    @jwt_required
    def get(self, username):
        try:
            user = User.objects.get(username=username)
        except DoesNotExist:
            return error_handler('User does not exist', 404)

        if get_jwt_identity() == user.username:
            schema = UserSchema()
        else:
            if user.private is True:
                return error_handler('Access forbidden', 403)
            else:
                schema = UserSchema(only=('username', 'name', 'avatar'))

        return schema.dump(user).data, 200

    @jwt_required
    def put(self, username):
        schema = UserSchema()

        try:
            user = User.objects.get(username=username)
        except DoesNotExist:
            return error_handler('User does not exist', 404)

        if get_jwt_identity() != user.username:
            return error_handler('Access forbidden', 403)

        try:
            user.update(**request.args.to_dict())
            user = User.objects.get(username=username)
        except NotUniqueError:
            return error_handler('Uniqueness error', 400)
        except ValidationError:
            return error_handler('Validation error', 400)

        return schema.dump(user).data, 200

    @jwt_required
    def delete(self, username):
        try:
            user = User.objects.get(username=username)
        except DoesNotExist:
            return error_handler('User does not exist', 404)

        if get_jwt_identity() != user.username:
            return error_handler('Access forbidden', 403)

        user.delete()
        return '', 204


class UserRegistrationResource(Resource):
    def post(self):
        schema = UserSchema()
        user = schema.load(request.args).data
        user.password = User.generate_hash(request.args['password'])

        try:
            user.save()
        except NotUniqueError:
            return error_handler('Uniqueness error', 400)
        except ValidationError:
            return error_handler('Validation error', 400)

        access_token = create_access_token(identity=request.args['username'])
        refresh_token = create_refresh_token(identity=request.args['username'])

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'metadata': schema.dump(user).data,
        }, 201


class UserLoginResource(Resource):
    def post(self):
        schema = UserSchema()
        user = schema.load(request.args).data
        user.password = User.generate_hash(request.args['password'])

        try:
            user = User.objects.get(username=request.args['username'])
        except DoesNotExist:
            return error_handler('User does not exist', 404)

        if User.verify_hash(request.args['password'], user.password):
            access_token = create_access_token(identity=request.args['username'])
            refresh_token = create_refresh_token(identity=request.args['username'])
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'metadata': schema.dump(user).data,
            }
        else:
            return error_handler('Wrong credentials', 401)


class RefreshTokenResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        username = get_jwt_identity()
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}




def error_handler(e, status):
    return {
        'status': status,
        'message': e,
    }, status
