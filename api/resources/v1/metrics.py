from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from ...models import Metric, User, Growthbook
from ...schemas import MetricSchema

from .responses import respond


class MetricListResource(Resource):
    @jwt_required
    def get(self):
        schema = MetricSchema(many=True, only=Fields.Metric.compact)
        if 'growthbook_id' in request.args:
            try:
                growthbook = Growthbook.objects.get(id=request.args['growthbook_id'])
            except (DoesNotExist, ValidationError) as e:
                return respond(404, {}, ['Growthbook does not exist', str(e)])
            if 'q' in request.args:
                metrics = Metric.objects(growthbook=growthbook, name__icontains=request.args['q'])
            else:
                metrics = Metric.objects(growthbook=growthbook)
        else:
            try:
                item = globals()[request.args['item_type']].objects.get(id=request.args['item_id'])
            except (DoesNotExist, ValidationError) as e:
                return respond(404, {}, ['Item does not exist', str(e)])
            growthbook = item.growthbook
            if 'q' in request.args:
                metrics = Metric.objects(item=item, name__icontains=request.args['q'])
            else:
                metrics = Metric.objects(item=item)

        if get_jwt_identity() not in growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        return respond(200, {'metrics': schema.dump(metrics).data})

    @jwt_required
    def post(self):
        schema = MetricSchema()
        metric = Metric(**schema.load(request.args).data)
        metric.user = User.objects.get(username=get_jwt_identity())
        try:
            metric.growthbook = Growthbook.objects.get(id=request.args['growthbook_id'])
        except (DoesNotExist, ValidationError) as e:
            return respond(404, {}, ['Growthbook does not exist', str(e)])
        if 'item_type' in request.args and 'item_id' in request.args:
            try:
                metric.item = globals()[request.args['item_type']].objects.get(id=request.args['item_id'])
            except (DoesNotExist, ValidationError) as e:
                return respond(404, {}, ['Item does not exist', str(e)])

        if get_jwt_identity() not in metric.growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        try:
            metric.save()
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(201, {'metric': schema.dump(metric).data})


class MetricResource(Resource):
    @jwt_required
    def get(self, id):
        try:
            metric = Metric.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Metric does not exist'])

        if get_jwt_identity() in metric.growthbook.collaborating_identities():
            schema = MetricSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        return respond(200, {'metric': schema.dump(metric).data})

    @jwt_required
    def put(self, id):
        try:
            metric = Metric.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Metric does not exist'])

        if get_jwt_identity() in metric.growthbook.collaborating_identities():
            schema = MetricSchema()
        else:
            return respond(403, {}, ['Access forbidden'])

        try:
            metric.update(**schema.dump(metric).data)
            # Return updated document
            metric = Metric.objects.get(id=id)
        except (NotUniqueError, ValidationError) as e:
            return respond(400, {}, ['Validation error', str(e)])

        return respond(200, {'metric': schema.dump(metric).data})

    @jwt_required
    def delete(self, id):
        try:
            metric = Metric.objects.get(id=id)
        except (DoesNotExist, ValidationError):
            return respond(404, {}, ['Metric does not exist'])

        if get_jwt_identity() not in metric.growthbook.collaborating_identities():
            return respond(403, {}, ['Access forbidden'])

        metric.delete()
        return respond(204)
