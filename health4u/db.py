from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    region = db.Column(db.String)
    # valid = db.Column(db.Boolean, nullable=True)


class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    region = db.Column(db.String)
    postcode = db.Column(db.String)
    telephone = db.Column(db.String)
    email = db.Column(db.String)
    website = db.Column(db.String)
    avg_time = db.Column(db.Interval)


class Department(db.Model):
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospital.id"), primary_key=True)
    department = db.Column(db.String, primary_key=True)


class OnDuty(db.Model):
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospital.id"), primary_key=True)
    department = db.Column(
        db.String, db.ForeignKey("department.department"), primary_key=True
    )
    date = db.Column(db.Date, primary_key=True, index=True)


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    need = db.Column(db.String)
    message = db.Column(db.String, nullable=False)

    # just for debug
    # def __repr__(self):
    #   return '<Request from {}, with email : {}. Subject of this request is : {}, and message : {}>'.format(self.name,self.email,self.need,self.message)
