from flask_restful import reqparse, Resource
from sqlalchemy.sql.expression import and_

from .db import Region, Hospital, Department, HasDepartment, OnDuty, object_as_dict
from .utils import to_date


class RegionResource(Resource):
    def get(self, id=None):
        if id is None:
            all_objects = [object_as_dict(reg) for reg in Region.query.all()]
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
            all_objects = [object_as_dict(dep) for dep in Department.query.all()]
            return {obj["id"]: obj for obj in all_objects}
        else:
            return object_as_dict(Department.query.filter_by(id=id).first())


filter_parser = reqparse.RequestParser()
filter_parser.add_argument("hospital_id", type=int)
filter_parser.add_argument("region_id", type=int)
filter_parser.add_argument("department_id", type=int)
filter_parser.add_argument("date", type=to_date)


class FilterRegionResource(Resource):
    def get(self):
        args = filter_parser.parse_args()
        region_query = Region.query.join(
            Hospital, Region.id == Hospital.region_id
        )
        if args["hospital_id"] is not None:
            region_query = region_query.filter_by(id=args["hospital_id"])
        if args["department_id"] is not None:
            region_query = region_query.join(
                HasDepartment, Hospital.id == HasDepartment.hospital_id
            ).filter_by(department_id=args["department_id"])
        if args["date"] is not None:
            if args["department_id"] is None:
                region_query = region_query.join(
                    OnDuty, Hospital.id == OnDuty.hospital_id
                )
            else:
                region_query = region_query.join(
                    OnDuty,
                    and_(
                        Hospital.id == OnDuty.hospital_id,
                        HasDepartment.department_id == OnDuty.department_id,
                    ),
                )
            region_query = region_query.filter_by(date=args["date"])

        all_objects = [object_as_dict(reg) for reg in region_query.all()]
        return {obj["id"]: obj for obj in all_objects}


class FilterHospitalResource(Resource):
    def get(self):
        args = filter_parser.parse_args()
        hospital_query = Hospital.query
        if args["region_id"] is not None:
            hospital_query = hospital_query.filter_by(region_id=args["region_id"])
        if args["department_id"] is not None:
            hospital_query = hospital_query.join(
                HasDepartment, Hospital.id == HasDepartment.hospital_id
            ).filter_by(department_id=args["department_id"])
        if args["date"] is not None:
            if args["department_id"] is None:
                hospital_query = hospital_query.join(
                    OnDuty, Hospital.id == OnDuty.hospital_id
                )
            else:
                hospital_query = hospital_query.join(
                    OnDuty,
                    and_(
                        Hospital.id == OnDuty.hospital_id,
                        HasDepartment.department_id == OnDuty.department_id,
                    ),
                )
            hospital_query = hospital_query.filter_by(date=args["date"])

        all_objects = [object_as_dict(hos) for hos in hospital_query.all()]
        return {obj["id"]: obj for obj in all_objects}


class FilterDepartmentResource(Resource):
    def get(self):
        args = filter_parser.parse_args()
        department_query = Department.query.join(
            HasDepartment, Department.id == HasDepartment.department_id
        ).join(
            Hospital, HasDepartment.hospital_id == Hospital.id
        )
        if args["hospital_id"] is not None:
            department_query = department_query.filter_by(id=args["hospital_id"])
        if args["region_id"] is not None:
            department_query = department_query.filter_by(region_id=args["region_id"])
        if args["date"] is not None:
            department_query = department_query.join(
                OnDuty,
                and_(
                    Hospital.id == OnDuty.hospital_id,
                    HasDepartment.department_id == OnDuty.department_id,
                ),
            ).filter_by(date=args["date"])

        all_objects = [object_as_dict(dep) for dep in department_query.all()]
        return {obj["id"]: obj for obj in all_objects}


class FilterHospitalResultsResource(Resource):
    def get(self):
        args = filter_parser.parse_args()
        hospital_query = Hospital.query
        if args["hospital_id"] is not None:
            hospital_query = hospital_query.filter_by(id=args["hospital_id"])
        if args["region_id"] is not None:
            hospital_query = hospital_query.filter_by(region_id=args["region_id"])
        if args["department_id"] is not None:
            hospital_query = hospital_query.join(
                HasDepartment, Hospital.id == HasDepartment.hospital_id
            ).filter_by(department_id=args["department_id"])
        if args["date"] is not None:
            if args["department_id"] is None:
                hospital_query = hospital_query.join(
                    OnDuty, Hospital.id == OnDuty.hospital_id
                )
            else:
                hospital_query = hospital_query.join(
                    OnDuty,
                    and_(
                        Hospital.id == OnDuty.hospital_id,
                        HasDepartment.department_id == OnDuty.department_id,
                    ),
                )
            hospital_query = hospital_query.filter_by(date=args["date"])

        all_objects = [object_as_dict(hos) for hos in hospital_query.all()]
        return {obj["id"]: obj for obj in all_objects}
