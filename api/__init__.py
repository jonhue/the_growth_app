from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from mongoengine import connect
import os

from .resources.v1 import *


connect('thegrowthapp', host='mongodb', port=27017)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
jwt = JWTManager(app)
api = Api(app)

api.add_resource(ActionItemListResource, '/v1/action_items')
api.add_resource(ActionItemResource, '/v1/action_items/<string:id>')
api.add_resource(ClientListResource, '/v1/clients')
api.add_resource(ClientResource, '/v1/clients/<string:id>')
api.add_resource(CollaborationListResource, '/v1/collaborations')
api.add_resource(CollaborationResource, '/v1/collaborations/<string:id>')
api.add_resource(EventListResource, '/v1/events')
api.add_resource(EventResource, '/v1/events/<string:id>')
api.add_resource(GoalListResource, '/v1/goals')
api.add_resource(GoalResource, '/v1/goals/<string:id>')
api.add_resource(GrowthbookListResource, '/v1/growthbooks')
api.add_resource(GrowthbookResource, '/v1/growthbooks/<string:id>')
api.add_resource(LogListResource, '/v1/logs')
api.add_resource(LogResource, '/v1/logs/<string:id>')
api.add_resource(MetricListResource, '/v1/metrics')
api.add_resource(MetricResource, '/v1/metrics/<string:id>')
api.add_resource(SchedulingListResource, '/v1/schedulings')
api.add_resource(SchedulingResource, '/v1/schedulings/<string:id>')
api.add_resource(RefreshTokenResource, '/v1/auth/refresh_token')
api.add_resource(UserListResource, '/v1/users')
api.add_resource(UserLoginResource, '/v1/auth/login')
api.add_resource(UserRegistrationResource, '/v1/auth/signup')
api.add_resource(UserResource, '/v1/users/<string:username>')
api.add_resource(WebhookSubscriptionListResource, '/v1/webhooks')
api.add_resource(WebhookSubscriptionResource, '/v1/webhooks/<string:id>')




@jwt.claims_verification_failed_loader
def claims_verification_failed_handler():
    return jsonify({
        'status': 'error',
        'code': 401,
        'messages': ['Claims verification failed'],
        'payload': {},
    }), 401

@jwt.expired_token_loader
def expired_token_handler():
    return jsonify({
        'status': 'error',
        'code': 401,
        'messages': ['Token expired'],
        'payload': {},
    }), 401

@jwt.invalid_token_loader
def invalid_token_handler(e):
    return jsonify({
        'status': 'error',
        'code': 401,
        'messages': ['Token invalid', str(e)],
        'payload': {},
    }), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_handler():
    return jsonify({
        'status': 'error',
        'code': 401,
        'messages': ['Fresh token needed'],
        'payload': {},
    }), 401

@jwt.revoked_token_loader
def revoked_token_handler():
    return jsonify({
        'status': 'error',
        'code': 401,
        'messages': ['Token revoked'],
        'payload': {},
    }), 401

@jwt.unauthorized_loader
def unauthorized_handler(e):
    return jsonify({
        'status': 'error',
        'code': 401,
        'messages': [str(e)],
        'payload': {},
    }), 401

@jwt.user_loader_error_loader
def user_loader_error_handler():
    return jsonify({
        'status': 'error',
        'code': 400,
        'messages': ['Error loading user'],
        'payload': {},
    }), 400
