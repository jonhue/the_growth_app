from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from ..models import Growthbook, User
from ..schemas import GrowthbookSchema

from .responses import respond


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
