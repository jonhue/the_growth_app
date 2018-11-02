from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from ...models import Scheduling
from ...schemas import SchedulingSchema

from .responses import respond


class SchedulingListResource(Resource):
    @jwt_required
    def post(self):
        schema = SchedulingSchema()
        scheduling = Scheduling(**schema.load(request.args).data)
        scheduling.user = User.objects.get(username=get_jwt_identity())
        try:
            task = globals()[request.args['task_type']].objects.get(id=request.args['task_id'])
        except (DoesNotExist, ValidationError) as e:
            return respond(404, {}, ['Task does not exist', str(e)])

        if get_jwt_identity() not in task.growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        try:
            task.scheduling = scheduling
            task.save()
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(201, {'scheduling': schema.dump(scheduling).data})


class SchedulingResource(Resource):
    @jwt_required
    def get(self, id):
        try:
            scheduling = Scheduling.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Scheduling does not exist'])

        if get_jwt_identity() in scheduling._instance.growthbook.collaborating_identities():
            schema = SchedulingSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        return respond(200, {'scheduling': schema.dump(scheduling).data})

    @jwt_required
    def put(self, id):
        try:
            scheduling = Scheduling.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Scheduling does not exist'])

        if get_jwt_identity() in scheduling._instance.growthbook.collaborating_identities():
            schema = SchedulingSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        try:
            scheduling.update(**schema.dump(scheduling).data)
            # Return updated document
            scheduling = Scheduling.objects.get(id=id)
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(200, {'scheduling': schema.dump(scheduling).data})

    @jwt_required
    def delete(self, id):
        try:
            scheduling = Scheduling.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Scheduling does not exist'])

        if get_jwt_identity() not in scheduling._instance.growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        scheduling.delete()
        return respond(204)
