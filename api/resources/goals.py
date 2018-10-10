from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from ..models import Goal, User, Growthbook
from ..schemas import GoalSchema

from .responses import respond


class GoalListResource(Resource):
    @jwt_required
    def post(self):
        schema = GoalSchema()
        goal = Goal(**schema.load(request.args).data)
        goal.user = User.objects.get(username=get_jwt_identity())
        goal.growthbook = Growthbook.objects.get(id=request.args['growthbook_id'])

        try:
            goal.save()
        except NotUniqueError as e:
            return respond(400, {}, ['Uniqueness error', str(e)])
        except ValidationError as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(201, {'goal': schema.dump(goal).data})


class GoalResource(Resource):
    @jwt_required
    def get(self, id):
        try:
            goal = Goal.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Goal does not exist'])

        if get_jwt_identity() in goal.growthbook.collaborating_identities():
            schema = GoalSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        return respond(200, {'goal': schema.dump(goal).data})

    @jwt_required
    def put(self, id):
        try:
            goal = Goal.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Goal does not exist'])

        if get_jwt_identity() in goal.growthbook.collaborating_identities():
            schema = GoalSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        try:
            goal.update(**schema.load(request.args).data)
            # Return update document
            goal = Goal.objects.get(id=id)
        except NotUniqueError as e:
            return respond(400, {}, ['Uniqueness error', str(e)])
        except ValidationError as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(200, {'goal': schema.dump(goal).data})

    @jwt_required
    def delete(self, id):
        try:
            goal = Goal.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Growthbook does not exist'])

        if get_jwt_identity() not in goal.growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        goal.delete()
        return respond(204)
