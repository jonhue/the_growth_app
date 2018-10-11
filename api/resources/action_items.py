from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from ..models import ActionItem, User, Growthbook, Goal
from ..schemas import ActionItemSchema

from .responses import respond


class ActionItemListResource(Resource):
    @jwt_required
    def post(self):
        schema = ActionItemSchema()
        action_item = ActionItem(**schema.load(request.args).data)
        action_item.user = User.objects.get(username=get_jwt_identity())
        try:
            action_item.growthbook = Growthbook.objects.get(id=request.args['growthbook_id'])
        except (DoesNotExist, ValidationError) as e:
            return respond(404, {}, ['Growthbook does not exist', str(e)])
        if 'parent_id' in request.args:
            try:
                action_item.parent = ActionItem.objects.get(id=request.args['parent_id'])
            except (DoesNotExist, ValidationError) as e:
                return respond(404, {}, ['Action item does not exist', str(e)])
        if 'goal_id' in request.args:
            try:
                action_item.goal = Goal.objects.get(id=request.args['goal_id'])
            except (DoesNotExist, ValidationError) as e:
                return respond(404, {}, ['Goal does not exist', str(e)])

        if get_jwt_identity() not in action_item.growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        try:
            action_item.save()
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(201, {'action_item': schema.dump(action_item).data})


class ActionItemResource(Resource):
    @jwt_required
    def get(self, id):
        try:
            action_item = ActionItem.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Action item does not exist'])

        if get_jwt_identity() in action_item.growthbook.collaborating_identities():
            schema = ActionItemSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        return respond(200, {'action_item': schema.dump(action_item).data})

    @jwt_required
    def put(self, id):
        try:
            action_item = ActionItem.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Action item does not exist'])

        if get_jwt_identity() in action_item.growthbook.collaborating_identities():
            schema = ActionItemSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        try:
            action_item.update(**schema.dump(action_item).data)
            # Return updated document
            action_item = ActionItem.objects.get(id=id)
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(200, {'action_item': schema.dump(action_item).data})

    @jwt_required
    def delete(self, id):
        try:
            action_item = ActionItem.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Action item does not exist'])

        if get_jwt_identity() not in action_item.growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        action_item.delete()
        return respond(204)
