from flask_restful import marshal_with, reqparse, Resource

from .db import Region, Hospital, Department, object_as_dict


class RegionResource(Resource):
    def get(self, id=None):
        if id is None:
            all_objects = [object_as_dict(hos) for hos in Region.query.all()]
            return {obj["id"]: obj for obj in all_objects}
        else:
            return object_as_dict(Region.query.filter_by(id=id).first())


class HospitalResource(Resource):
    def get(self, id=None):
        if id is None:
            all_objects = [object_as_dict(hos) for hos in Hospital.query.all()]
            return {obj["id"]: obj for obj in all_objects}
        else:
            return object_as_dict(Hospital.query.filter_by(id=id).first())


class DepartmentResource(Resource):
    def get(self, id=None):
        if id is None:
            all_objects = [object_as_dict(hos) for hos in Department.query.all()]
            return {obj["id"]: obj for obj in all_objects}
        else:
            return object_as_dict(Department.query.filter_by(id=id).first())
