from datetime import datetime

import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_babel import Babel
from flask_babel import gettext
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from werkzeug.security import generate_password_hash, check_password_hash

from .api import RegionResource, HospitalResource, DepartmentResource, FilterHospitalResource, FilterRegionResource, \
    FilterDepartmentResource, FilterHospitalResultsResource
from .db import db, User, Hospital, Department, OnDuty, Request
from .init_db import load_data


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.app_context().push()
    app.secret_key = "gfdskjn@/r31ff@#%g45"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)
    db.create_all()
    if db.session.query(Hospital).count() == 0:
        load_data()

    login_manager = LoginManager()
    login_manager.login_view = "log_in"
    login_manager.login_message_category = "danger"
    login_manager.init_app(app)

    api = Api(app, "/api/v1")
    api.add_resource(RegionResource, "/region", "/region/", "/region/<int:id>")
    api.add_resource(HospitalResource, "/hospital", "/hospital/", "/hospital/<int:id>")
    api.add_resource(DepartmentResource, "/department", "/department/", "/department/<int:id>")
    api.add_resource(FilterRegionResource, "/region_filter", "/region_filter/")
    api.add_resource(FilterHospitalResource, "/hospital_filter", "/hospital_filter/")
    api.add_resource(FilterDepartmentResource, "/department_filter", "/department_filter/")
    api.add_resource(FilterHospitalResultsResource, "/hospital_results", "/hospital_results/")

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        translations = [str(translation) for translation in babel.list_translations()]
        if "lang" in request.cookies and request.cookies["lang"] in translations:
            return request.cookies["lang"]
        return request.accept_languages.best_match(translations, default="en")

    app.jinja_env.globals["get_locale"] = get_locale
    app.jinja_env.globals["req_datetime"] = datetime.now()

    @app.route("/")
    @app.route("/home")
    def home():
        return render_template("home.html")

    @app.route("/hospitals")
    def hospitals():
        return render_template("hospitals.html")

    @app.route("/contact_us", methods=["POST", "GET"])
    def contact_us():
        if flask.request.method == "GET":
            return render_template("contact_us.html")
        elif flask.request.method == "POST":
            rname = request.form["contact-name"]
            remail = request.form["contact-email"]
            rneed = request.form["contact-need"]
            rmessage = request.form["contact-message"]

            new_req = Request(name=rname, email=remail, need=rneed, message=rmessage)

            db.session.add(new_req)
            db.session.commit()

            flash(gettext("Successful Msg"), "success")
            return redirect(url_for("contact_us"))

    @app.route("/covid19")
    def covid19():
        return render_template("covid19.html")

    @app.route("/log_in", methods=["POST", "GET"])
    def log_in():
        if current_user.is_authenticated:
            flash(gettext("Already logged in"), "info")
            return redirect(url_for("home"))

        if flask.request.method == "GET":
            return render_template("log_in.html")
        elif flask.request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            temp_user = User.query.filter_by(email=email).first()

            if temp_user is not None and check_password_hash(temp_user.password, password):
                flash(gettext("Successful log in"), "success")
                login_user(temp_user)
                return redirect(url_for("home"))
            else:
                flash(gettext("Wrong Credentials"), "danger")
                return redirect(url_for("log_in"))

    @app.route("/sign_up", methods=["POST", "GET"])
    def sign_up():
        if current_user.is_authenticated:
            flash(gettext("Already logged in"), "info")
            return redirect(url_for("home"))

        if flask.request.method == "GET":
            return render_template("sign_up.html")
        elif flask.request.method == "POST":
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            region_id = request.form["region"]
            email = request.form["email"]
            password = request.form["password"]
            confirm = request.form["confirm-password"]

            existing_user = User.query.filter_by(email=email).first()

            if existing_user is None:
                if password == confirm:
                    new_user = User(first_name=first_name, last_name=last_name, region_id=int(region_id), email=email,
                                    password=generate_password_hash(password, method="sha256"))
                    db.session.add(new_user)
                    db.session.commit()
                    flash(gettext("Successful registration"), "success")
                    return redirect(url_for('log_in'))
                flash(gettext("Not matched passwords"), "danger")
                return redirect(url_for("sign_up"))

            flash(gettext("Existed email"), "danger")
            return redirect(url_for("sign_up"))

    @app.route("/change_password", methods=["POST", "GET"])
    @login_required
    def change_password():
        if flask.request.method == "GET":
            return render_template("change_password.html")
        elif flask.request.method == "POST":
            password = request.form["old_password"]
            new_password = request.form["new_password"]
            conf_new_pass = request.form["conf_new_password"]

            if check_password_hash(current_user.password, password) and new_password == conf_new_pass:
                current_user.password = generate_password_hash(new_password, method="sha256")
                db.session.add(current_user)
                db.session.commit()

                flash(gettext("Successful password change"), "success")
                return redirect(url_for('home'))
            else:
                flash(gettext("Something went wrong"), "danger")
                return redirect(url_for("change_password"))

    @app.route("/account_details", methods=["POST", "GET"])
    @login_required
    def account_details():
        if flask.request.method == "GET":
            return render_template("account_details.html")
        elif flask.request.method == "POST":
            email = request.form["email"]
            existing_user = User.query.filter_by(email=email).first()

            if existing_user is None or current_user.email == email:
                current_user.first_name = request.form["first_name"]
                current_user.last_name = request.form["last_name"]
                current_user.region_id = request.form["region_account"]
                current_user.email = request.form["email"]

                db.session.add(current_user)
                db.session.commit()

                flash(gettext("Successful details update"), 'success')
                return redirect(url_for("home"))
            else:
                flash(gettext("Existed email"), "danger")
                return redirect(url_for("account_details"))

    @app.route("/delete_account")
    @login_required
    def delete_account():

        User.query.filter(User.id == current_user.id).delete()
        db.session.commit()

        logout_user()

        flash(gettext("Successful account delete"), "success")
        return redirect(url_for("home"))

    @app.route("/forgot_password", methods=["POST", "GET"])
    def forgot_password():
        if current_user.is_authenticated:
            flash(gettext("Logout to access page"), "info")
            return redirect(url_for("home"))

        if flask.request.method == "GET":
            return render_template("forgot_password.html")
        elif flask.request.method == "POST":
            email = request.form["email"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            region_id = request.form["region_forgot"]

            temp_user = User.query\
                .filter_by(email=email)\
                .filter_by(first_name=first_name)\
                .filter_by(last_name=last_name)\
                .filter_by(region_id=region_id)\
                .first()

            if temp_user:
                new_req = Request(email=temp_user.email, name=temp_user.last_name, need='-1', message='-1')
                db.session.add(new_req)
                db.session.commit()
                flash(gettext("Successful request submit"), "success")
                return redirect(url_for('home'))
            else:
                flash(gettext("Wrong Credentials"), "danger")
                return redirect(url_for("forgot_password"))

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("log_in"))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(Exception)
    def page_not_found(e):
        return render_template("error.html"), 400

    app.register_error_handler(400, page_not_found)

    return app


app = create_app()
