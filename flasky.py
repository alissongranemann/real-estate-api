import os
from dotenv import load_dotenv
from app import create_app, db  # noqa: F401
from app.models import Property, Location  # noqa: F401

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = create_app(os.environ["APP_SETTINGS"])


if __name__ == "__main__":
    app.run()
