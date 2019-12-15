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

from app.models import (
    FederalUnity,
    City,
    Neighbourhood,
    Street,
    Property,
    Location,
    PostalCode,
)

Swagger(app, template_file="docs/properties_template.yml")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)
logging.getLogger("werkzeug").setLevel(logging.INFO)

if __name__ == "__main__":
    app.run()
