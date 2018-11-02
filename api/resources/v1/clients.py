from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from ...models import Client, User
from ...schemas import ClientSchema

from .responses import respond


class ClientListResource(Resource):
    @jwt_required
    def get(self):
        schema = ClientSchema(many=True, only=Fields.Client.compact)
        user = User.objects.get(username=get_jwt_identity())
        subscriptions = WebhookSubscription.objects.get(user=user)
        clients = set(subscription.client for subscription in subscriptions)

        return respond(200, {'clients': schema.dump(clients).data})

    @jwt_required
    def post(self):
        schema = ClientSchema()
        client = Client(**schema.load(request.args).data)
        client.user = User.objects.get(username=get_jwt_identity())

        try:
            client.save()
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(201, {'client': schema.dump(client).data})


class ClientResource(Resource):
    @jwt_required
    def get(self, id):
        try:
            client = Client.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Client does not exist'])

        if get_jwt_identity() == client.user.username:
            schema = ClientSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        return respond(200, {'client': schema.dump(client).data})

    @jwt_required
    def put(self, id):
        try:
            client = Client.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Client does not exist'])

        if get_jwt_identity() in client.user.username:
            schema = ClientSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        try:
            client.update(**schema.load(request.args).data)
            # Return updated document
            client = Client.objects.get(id=id)
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(200, {'client': schema.dump(client).data})

    @jwt_required
    def delete(self, id):
        try:
            client = Client.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Client does not exist'])

        if get_jwt_identity() not in client.user.username:
            return respond(403, {}, ['Access forbidden'])

        client.delete()
        return respond(204)
