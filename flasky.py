# flake8: noqa
import os
from dotenv import load_dotenv
from app import create_app, db

from flasgger import Swagger
import logging

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.environ["APP_SETTINGS"])

from app.models import FederalUnity, City, Neighbourhood, Street, Property, Location

template = {
    "swagger": "2.0",
    "info": {
        "title": "Real Estate API",
        "description": "An API for real estate prices",
        "contact": {
            "responsibleOrganization": "ME",
            "responsibleDeveloper": "Me",
            "email": "alissongranemannabreu@gmail.com",
            "url": "www.github.com/alissongranemann",
        },
        "version": "0.0.1",
    },
    "schemes": ["http", "https"],
}

swagger = Swagger(app, template=template)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)
logging.getLogger("werkzeug").setLevel(logging.INFO)

if __name__ == "__main__":
    app.run()
