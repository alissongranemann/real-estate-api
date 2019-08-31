import os
from dotenv import load_dotenv
from app import create_app, db  # noqa: F401
from app.models import Property, Location  # noqa: F401
import logging

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = create_app(os.environ["APP_SETTINGS"])

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)
logging.getLogger("werkzeug").setLevel(logging.INFO)

if __name__ == "__main__":
    app.run()
