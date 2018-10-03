from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from mongoengine import connect
import os

from .resources import *


connect('thegrowthapp', host='mongodb', port=27017)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
jwt = JWTManager(app)
api = Api(app)

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<string:username>')
api.add_resource(UserRegistrationResource, '/auth/signup')
api.add_resource(UserLoginResource, '/auth/login')
api.add_resource(RefreshTokenResource, '/auth/refresh_token')




@jwt.claims_verification_failed_loader
def claims_verification_failed_handler():
    return jsonify({
        'status': 401,
        'message': 'Claims verification failed'
    }), 401

@jwt.expired_token_loader
def expired_token_handler():
    return jsonify({
        'status': 401,
        'message': 'Token expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_handler(e):
    return jsonify({
        'status': 401,
        'message': 'Token invalid'
    }), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_handler():
    return jsonify({
        'status': 401,
        'message': 'Fresh token needed'
    }), 401

@jwt.revoked_token_loader
def revoked_token_handler():
    return jsonify({
        'status': 401,
        'message': 'Token revoked'
    }), 401

@jwt.unauthorized_loader
def unauthorized_handler():
    return jsonify({
        'status': 401,
        'message': 'Unauthorized'
    }), 401

@jwt.user_loader_error_loader
def user_loader_error_handler():
    return jsonify({
        'status': 400,
        'message': 'Error loading user'
    }), 400
