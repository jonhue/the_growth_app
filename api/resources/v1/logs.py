from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from ...models import Log, Goal
from ...schemas import LogSchema

from .responses import respond


class LogListResource(Resource):
    @jwt_required
    def get(self):
        schema = LogSchema(many=True, only=Fields.Log.compact)
        try:
            goal = Goal.objects.get(id=request.args['goal_id'])
        except (DoesNotExist, ValidationError) as e:
            return respond(404, {}, ['Goal does not exist', str(e)])
        logs = goal.logs

        if get_jwt_identity() not in goal.growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        return respond(200, {'logs': schema.dump(logs).data})

    @jwt_required
    def post(self):
        schema = LogSchema()
        log = Log(**schema.load(request.args).data)
        log.user = User.objects.get(username=get_jwt_identity())
        try:
            goal = Goal.objects.get(id=request.args['goal_id'])
        except (DoesNotExist, ValidationError) as e:
            return respond(404, {}, ['Goal does not exist', str(e)])

        if get_jwt_identity() not in goal.growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        try:
            goal.logs.append(log)
            goal.save()
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(201, {'log': schema.dump(log).data})


class LogResource(Resource):
    @jwt_required
    def get(self, id):
        try:
            log = Log.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Log does not exist'])

        if get_jwt_identity() in log._instance.collaborating_identities():
            schema = LogSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        return respond(200, {'log': schema.dump(log).data})

    @jwt_required
    def put(self, id):
        try:
            log = Log.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Log does not exist'])

        if get_jwt_identity() in log._instance.collaborating_identities():
            schema = LogSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        try:
            log.update(**schema.dump(log).data)
            # Return updated document
            log = Log.objects.get(id=id)
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(200, {'log': schema.dump(log).data})

    @jwt_required
    def delete(self, id):
        try:
            log = Log.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Log does not exist'])

        if get_jwt_identity() not in log._instance.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        log.delete()
        return respond(204)
