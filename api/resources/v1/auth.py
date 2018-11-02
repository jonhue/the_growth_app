from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_refresh_token_required
from flask_restful import Resource

from ...models import User, Client
from ...schemas import UserSchema

from .responses import respond


class UserRegistrationResource(Resource):
    def post(self):
        schema = UserSchema()
        user = User(**schema.load(request.args).data)
        user.password = User.generate_hash(request.args['password'])

        try:
            user.save()
        except (NotUniqueError, ValidationError) as e:
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
