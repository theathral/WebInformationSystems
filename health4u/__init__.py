from datetime import datetime
from types import SimpleNamespace

from flask import Flask, render_template


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    @app.route("/")
    @app.route("/home")
    def home():
        return render_template("home.html", req_datetime=datetime.now())

    @app.route("/hospitals")
    def hospitals():
        return render_template("hospitals.html", req_datetime=datetime.now())

    @app.route("/on_duty")
    def on_duty():
        return render_template("on_duty.html", req_datetime=datetime.now())

    @app.route("/contact_us")
    def contact_us():
        return render_template("contact_us.html", req_datetime=datetime.now())


    @app.route("/covid19")
    def covid19():
        return render_template("covid19.html", req_datetime=datetime.now())

    @app.route("/log_in")
    def log_in():
        return render_template("log_in.html", req_datetime=datetime.now())

    @app.route("/sign_up")
    def sign_up():
        return render_template("sign_up.html", req_datetime=datetime.now())

    return app


app = create_app()
