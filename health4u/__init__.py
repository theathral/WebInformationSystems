from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .db import create_db


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.secret_key = 'gfdskjn@/r31ff@#%g45'
    db, db_models = create_db(app)
    User = db_models["user"]
    Request = db_models["request"]
    db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

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
                flash('Registration was Successful. Please Log in.','success')
                return redirect(url_for('log_in'))
            flash('Passwords do not match. Please try again.','danger')
            return redirect(url_for('sign_up'))

        flash('Email address already exists.','danger')
        return redirect(url_for('sign_up'))

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        email = request.form['email']
        password = request.form['password']

        temp_user = User.query.filter_by(email=email).first()

        if temp_user is not None and check_password_hash(temp_user.password, password):
            flash('You have successfully logged in!','success')
            login_user(temp_user)
            return redirect(url_for('home'))
        else:
            flash('Wrong Credentials','danger')
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
            flash('Warning : No message included!','danger')
            return redirect(url_for('contact_us'))
        new_Req = Request(name=rname, email=remail, need=rneed, message=rmessage)
        #print(new_Req)
        db.session.add(new_Req)
        db.session.commit()

        flash('Message sent successfully!','success')
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

    return app


app = create_app()
