from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin


def create_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db = SQLAlchemy(app)

    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String, unique=True, nullable=False)
        password = db.Column(db.String, nullable=False)
        first_name = db.Column(db.String)
        last_name = db.Column(db.String)
        region = db.Column(db.String)
        #valid = db.Column(db.Boolean, nullable=True)

    class Hospital(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, nullable=False)
        address = db.Column(db.String)
        region = db.Column(db.String)
        telephone = db.Column(db.String)
        email = db.Column(db.String)
        website = db.Column(db.String)
        avg_time = db.Column(db.Interval)

    class Department(db.Model):
        hospital_id = db.Column(db.Integer, primary_key=True)
        department = db.Column(db.Integer, primary_key=True)
        
    class Request(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String)
        email = db.Column(db.String)
        need = db.Column(db.String)
        message = db.Column(db.String, nullable=False)

    return (
        db,
        {Model.__table__.name.lower(): Model for Model in (User, Hospital, Department, Request)},
    )
