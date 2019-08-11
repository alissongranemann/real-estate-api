import os
from flask import Flask
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

import sys
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import Property, Address

app = create_app(os.environ["APP_SETTINGS"])
migrate = Migrate(app, db)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()


if __name__ == "__main__":
    app.run()
