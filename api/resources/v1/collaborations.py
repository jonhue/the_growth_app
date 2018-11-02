from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from ...models import Collaboration
from ...schemas import CollaborationSchema

from .responses import respond


class CollaborationListResource(Resource):
    @jwt_required
    def get(self):
        schema = CollaborationSchema(many=True, only=Fields.Collaboration.compact)
        try:
            growthbook = Growthbook.objects.get(id=request.args['growthbook_id'])
        except (DoesNotExist, ValidationError) as e:
            return respond(404, {}, ['Growthbook does not exist', str(e)])
        collaborations = growthbook.collaborations

        if get_jwt_identity() not in growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        return respond(200, {'collaborations': schema.dump(collaborations).data})

    @jwt_required
    def post(self):
        schema = CollaborationSchema()
        collaboration = Collaboration(**schema.load(request.args).data)
        collaboration.inviter = User.objects.get(username=get_jwt_identity())
        try:
            collaboration.invited = User.objects.get(username=request.args['username'])
        except (DoesNotExist, ValidationError) as e:
            return respond(404, {}, ['User does not exist', str(e)])
        try:
            growthbook = Growthbook.objects.get(id=request.args['growthbook_id'])
        except (DoesNotExist, ValidationError) as e:
            return respond(404, {}, ['Growthbook does not exist', str(e)])

        if get_jwt_identity() not in growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        try:
            growthbook.collaborations.append(collaboration)
            growthbook.save()
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(201, {'collaboration': schema.dump(collaboration).data})


class CollaborationResource(Resource):
    @jwt_required
    def get(self, id):
        try:
            collaboration = Collaboration.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Collaboration does not exist'])

        if get_jwt_identity() in collaboration._instance.collaborating_identities():
            schema = CollaborationSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        return respond(200, {'collaboration': schema.dump(collaboration).data})

    @jwt_required
    def put(self, id):
        try:
            collaboration = Collaboration.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Collaboration does not exist'])

        if get_jwt_identity() in collaboration._instance.collaborating_identities():
            schema = CollaborationSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        try:
            collaboration.update(**schema.dump(collaboration).data)
            # Return updated document
            collaboration = Collaboration.objects.get(id=id)
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(200, {'collaboration': schema.dump(collaboration).data})

    @jwt_required
    def delete(self, id):
        try:
            collaboration = Collaboration.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Collaboration does not exist'])

        if get_jwt_identity() not in collaboration._instance.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        collaboration.delete()
        return respond(204)
