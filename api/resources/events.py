from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from ..models import Event
from ..schemas import EventSchema

from .responses import respond


class EventListResource(Resource):
    @jwt_required
    def post(self):
        schema = EventSchema()
        event = Event(**schema.load(request.args).data)
        event.user = User.objects.get(username=get_jwt_identity())
        try:
            task = globals()[request.args['task_type']].objects.get(id=request.args['task_id'])
        except (DoesNotExist, ValidationError) as e:
            return respond(404, {}, ['Task does not exist', str(e)])

        if get_jwt_identity() not in task.growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        try:
            task.events.append(event)
            task.save()
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(201, {'event': schema.dump(event).data})


class EventResource(Resource):
    @jwt_required
    def get(self, id):
        try:
            event = Event.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Event does not exist'])

        if get_jwt_identity() in event._instance.growthbook.collaborating_identities():
            schema = EventSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        return respond(200, {'event': schema.dump(event).data})

    @jwt_required
    def put(self, id):
        try:
            event = Event.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Event does not exist'])

        if get_jwt_identity() in event._instance.growthbook.collaborating_identities():
            schema = EventSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        try:
            event.update(**schema.dump(event).data)
            # Return updated document
            event = Event.objects.get(id=id)
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(200, {'event': schema.dump(event).data})

    @jwt_required
    def delete(self, id):
        try:
            event = Event.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Event does not exist'])

        if get_jwt_identity() not in event._instance.growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        event.delete()
        return respond(204)
