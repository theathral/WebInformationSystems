from datetime import datetime

import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from flask_babel import Babel
from werkzeug.security import generate_password_hash, check_password_hash

from .api import RegionResource, HospitalResource, DepartmentResource, FilterResource
from .db import db, User, Hospital, Department, OnDuty, Request
from .init_db import load_data


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.app_context().push()
    app.secret_key = 'gfdskjn@/r31ff@#%g45'

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)
    db.create_all()
    if db.session.query(Hospital).count() == 0:
        load_data()

    login_manager = LoginManager()
    login_manager.login_view = 'log_in'
    login_manager.login_message_category = "danger"
    login_manager.init_app(app)

    api = Api(app, "/api/v1")
    api.add_resource(RegionResource, "/region", "/region/", "/region/<int:id>")
    api.add_resource(HospitalResource, "/hospital", "/hospital/", "/hospital/<int:id>")
    api.add_resource(DepartmentResource, "/department", "/department/", "/department/<int:id>")
    api.add_resource(FilterResource, "/filter", "/filter/")

    babel = Babel(app)
    @babel.localeselector
    def get_locale():
        translations = [str(translation) for translation in babel.list_translations()]
        if "lang" in request.cookies and request.cookies["lang"] in translations:
            return request.cookies["lang"]
        return request.accept_languages.best_match(translations, default="en")

    @app.route("/")
    @app.route("/home")
    def home():
        return render_template("home.html", req_datetime=datetime.now())

    @app.route("/hospitals")
    def hospitals():
        return render_template("hospitals.html", req_datetime=datetime.now())

    @app.route("/contact_us", methods=['POST', 'GET'])
    def contact_us():
        if flask.request.method == 'GET':
            return render_template("contact_us.html", req_datetime=datetime.now())
        elif flask.request.method == 'POST':
            rname = request.form['contact-name']
            remail = request.form['contact-email']
            rneed = request.form['contact-need']
            rmessage = request.form['contact-message']

            if rmessage == "":
                flash('Warning : No message included!', 'danger')
                return redirect(url_for('contact_us'))
            new_Req = Request(name=rname, email=remail, need=rneed, message=rmessage)

            db.session.add(new_Req)
            db.session.commit()

            flash('Message sent successfully!', 'success')
            return redirect(url_for('contact_us'))

    @app.route("/covid19")
    def covid19():
        return render_template("covid19.html", req_datetime=datetime.now())

    @app.route("/log_in", methods=['POST', 'GET'])
    def log_in():
        if current_user.is_authenticated:
            flash('You are already logged in!', 'info')
            return redirect(url_for('home'))

        if flask.request.method == 'GET':
            return render_template("log_in.html", req_datetime=datetime.now())
        elif flask.request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            temp_user = User.query.filter_by(email=email).first()

            if temp_user is not None and check_password_hash(temp_user.password, password):
                flash('You have successfully logged in!', 'success')
                login_user(temp_user)
                return redirect(url_for('home'))
            else:
                flash('Wrong Credentials', 'danger')
                return redirect(url_for('log_in'))

    @app.route("/sign_up", methods=['POST', 'GET'])
    def sign_up():
        if current_user.is_authenticated:
            flash('You are already logged in!', 'info')
            return redirect(url_for('home'))

        if flask.request.method == 'GET':
            return render_template("sign_up.html", req_datetime=datetime.now())
        elif flask.request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            region_id = request.form['region']
            email = request.form['email']
            password = request.form['password']
            confirm = request.form['confirm-password']

            existing_user = User.query.filter_by(email=email).first()

            if existing_user is None:
                if password == confirm:
                    new_user = User(first_name=first_name, last_name=last_name, region_id=int(region_id), email=email,
                                    password=generate_password_hash(password, method='sha256'))
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Registration was Successful. Please Log in.', 'success')
                    return redirect(url_for('log_in'))
                flash('Passwords do not match. Please try again.', 'danger')
                return redirect(url_for('sign_up'))

            flash('Email address already exists.', 'danger')
            return redirect(url_for('sign_up'))

    @app.route("/change_password", methods=['POST', 'GET'])
    @login_required
    def change_password():
        if flask.request.method == 'GET':
            return render_template("change_password.html", req_datetime=datetime.now())
        elif flask.request.method == 'POST':
            password = request.form['old_password']
            new_password = request.form['new_password']
            conf_new_pass = request.form['conf_new_password']

            if check_password_hash(current_user.password, password) and new_password == conf_new_pass:
                current_user.password = generate_password_hash(new_password, method='sha256')
                db.session.add(current_user)
                db.session.commit()

                flash('Password changed successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Something went wrong. Try again', 'danger')
                return redirect(url_for('change_password'))

    @app.route("/account_details", methods=['POST', 'GET'])
    @login_required
    def account_details():
        if flask.request.method == 'GET':
            return render_template("account_details.html", req_datetime=datetime.now())
        elif flask.request.method == 'POST':
            email = request.form['email']
            existing_user = User.query.filter_by(email=email).first()

            if existing_user is None or current_user.email == email:
                current_user.first_name = request.form['first_name']
                current_user.last_name = request.form['last_name']
                current_user.region_id = request.form['region_account']
                current_user.email = request.form['email']

                db.session.add(current_user)
                db.session.commit()

                flash('Account details changed successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('This email already exists. Try again', 'danger')
                return redirect(url_for('account_details'))

    @app.route("/deleteUser")
    @login_required
    def delete_account():

        User.query.filter(User.id == current_user.id).delete()
        db.session.commit()

        logout_user()

        flash('Your account has been successfully deleted.', 'success')
        return redirect(url_for('home'))

    @app.route("/forgot_password", methods=['POST', 'GET'])
    def forgot_password():
        if current_user.is_authenticated:
            flash('Logout to access this page!', 'info')
            return redirect(url_for('home'))

        if flask.request.method == 'GET':
            return render_template("forgot_password.html", req_datetime=datetime.now())
        elif flask.request.method == 'POST':
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            region_id = request.form['region_forgot']

            temp_user = User.query.filter_by(email=email).first()

            if temp_user and temp_user.email == email and temp_user.first_name == first_name and temp_user.last_name == last_name and temp_user.region_id == region_id:
                new_req = Request(email=temp_user.email, name=temp_user.last_name, need='-1', message='-1')
                db.session.add(new_req)
                db.session.commit()
                flash('Your request has been submitted. Someone will contact you soon!', 'success')
                return redirect(url_for('home'))
            else:
                flash('No user found with these credentials', 'danger')
                return redirect(url_for('forgot_password'))

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('log_in'))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # @app.errorhandler(Exception)
    # def page_not_found(e):
    #     return render_template('error.html'), 400

    # app.register_error_handler(400, page_not_found)

    return app


app = create_app()
