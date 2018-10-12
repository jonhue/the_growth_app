from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from ..models import WebhookSubscription, User, Client
from ..schemas import WebhookSubscriptionSchema

from .responses import respond


class WebhookSubscriptionListResource(Resource):
    @jwt_required
    def post(self):
        schema = WebhookSubscriptionSchema()
        subscription = WebhookSubscription(**schema.load(request.args).data)
        subscription.user = User.objects.get(username=get_jwt_identity())
        try:
            subscription.client = Client.objects.get(id=request.args['client_id'])
        except (DoesNotExist, ValidationError) as e:
            return respond(404, {}, ['Client does not exist', str(e)])

        try:
            subscription.save()
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(201, {'subscription': schema.dump(subscription).data})


class WebhookSubscriptionResource(Resource):
    @jwt_required
    def get(self, id):
        try:
            subscription = WebhookSubscription.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Subscription does not exist'])

        if get_jwt_identity() == subscription.client.user.username:
            schema = WebhookSubscriptionSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        return respond(200, {'subscription': schema.dump(subscription).data})

    @jwt_required
    def put(self, id):
        try:
            subscription = WebhookSubscription.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Subscription does not exist'])

        if get_jwt_identity() in subscription.client.user.username:
            schema = WebhookSubscriptionSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        try:
            subscription.update(**schema.load(request.args).data)
            # Return updated document
            subscription = WebhookSubscription.objects.get(id=id)
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(200, {'subscription': schema.dump(subscription).data})

    @jwt_required
    def delete(self, id):
        try:
            client = WebhookSubscription.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Subscription does not exist'])

        if get_jwt_identity() not in client.user.username:
            return respond(403, {}, ['Access forbidden'])

        client.delete()
        return respond(204)
