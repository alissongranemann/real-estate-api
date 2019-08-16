from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .api import api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    @app.route("/", methods=["GET"])
    def home():
        return "Up and running!", 200

    return app
