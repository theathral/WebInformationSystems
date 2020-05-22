from flask_restful import Resource

from .db import Hospital, object_as_dict

class HospitalResource(Resource):
    def get(self, id=None):
        if id is None:
            return [object_as_dict(hos) for hos in Hospital.query.all()]
        else:
            return object_as_dict(Hospital.query.filter_by(id=id).first())
