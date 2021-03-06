from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.schema import ForeignKeyConstraint

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    region_id = db.Column(db.Integer, db.ForeignKey("region.id"))


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    name_en = db.Column(db.String)


class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey("region.id"))
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    postcode = db.Column(db.String)
    telephone = db.Column(db.String)
    email = db.Column(db.String)
    website = db.Column(db.String)
    name_en = db.Column(db.String)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    name_en = db.Column(db.String)


class HasDepartment(db.Model):
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospital.id"), primary_key=True)
    department_id = db.Column(
        db.Integer, db.ForeignKey("department.id"), primary_key=True
    )


class OnDuty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    hospital_id = db.Column(db.Integer)
    department_id = db.Column(db.Integer)

    __table_args__ = (
        ForeignKeyConstraint(
            ["hospital_id", "department_id"],
            ["has_department.hospital_id", "has_department.department_id"],
        ),
    )


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    need = db.Column(db.String)
    message = db.Column(db.String, nullable=False)

    # just for debug
    # def __repr__(self):
    #   return '<Request from {}, with email : {}. Subject of this request is : {}, and message : {}>'.format(self.name,self.email,self.need,self.message)


# Nabbed from https://stackoverflow.com/a/37350445
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
