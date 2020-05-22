from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .db import db, User, Hospital, Department, OnDuty, Request
from .api import HospitalResource
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
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    api = Api(app, "/api/v1")
    api.add_resource(HospitalResource, "/hospital", "/hospital/<int:id>")

    @app.route("/")
    @app.route("/home")
    def home():
        return render_template("home.html", req_datetime=datetime.now())

    @app.route("/hospitals")
    def hospitals():
        return render_template("hospitals.html", req_datetime=datetime.now())

    @app.route("/contact_us")
    def contact_us():
        return render_template("contact_us.html", req_datetime=datetime.now())

    @app.route("/covid19")
    def covid19():
        return render_template("covid19.html", req_datetime=datetime.now())

    @app.route("/log_in", methods=['POST', 'GET'])
    def log_in():
        return render_template("log_in.html", req_datetime=datetime.now())

    @app.route("/sign_up")
    def sign_up():
        return render_template("sign_up.html", req_datetime=datetime.now())

    @app.route("/change_password", methods=['POST', 'GET'])
    def change_password():
        return render_template("change_password.html", req_datetime=datetime.now())

    @app.route("/account_details", methods=['POST', 'GET'])
    def account_details():
        return render_template("account_details.html", req_datetime=datetime.now())

    @app.route("/signUp", methods=['POST', 'GET'])
    def signUp():
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        region = request.form['region']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm-password']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user is None:
            if password == confirm:
                new_user = User(first_name=first_name, last_name=last_name, region=region, email=email,
                                password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                flash('Registration was Successful. Please Log in.', 'success')
                return redirect(url_for('log_in'))
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('sign_up'))

        flash('Email address already exists.', 'danger')
        return redirect(url_for('sign_up'))

    @app.route('/login', methods=['POST', 'GET'])
    def login():
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

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('log_in'))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/contactUs", methods=['POST', 'GET'])
    def contactUs():
        rname = request.form['contact-name']
        remail = request.form['contact-email']
        rneed = request.form['contact-need']
        rmessage = request.form['contact-message']

        if rmessage == "":
            flash('Warning : No message included!', 'danger')
            return redirect(url_for('contact_us'))
        new_Req = Request(name=rname, email=remail, need=rneed, message=rmessage)
        # print(new_Req)
        db.session.add(new_Req)
        db.session.commit()

        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact_us'))

    @app.route("/changePassword", methods=['POST', 'GET'])
    def changePassword():
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

    @app.route("/accountDetails", methods=['POST', 'GET'])
    def accountDetails():
        email = request.form['email']
        existing_user = User.query.filter_by(email=email).first()

        if existing_user is None or current_user.email == email:
            current_user.first_name = request.form['first_name']
            current_user.last_name = request.form['last_name']
            current_user.region = request.form['region']
            current_user.email = request.form['email']

            db.session.add(current_user)
            db.session.commit()
            flash('Account details changed successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('This email already exists. Try again', 'danger')
            return redirect(url_for('account_details'))

    @app.errorhandler(Exception)
    def page_not_found(e):
        return render_template('error.html'), 400

    app.register_error_handler(400, page_not_found)

    return app


app = create_app()
