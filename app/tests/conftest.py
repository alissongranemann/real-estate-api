import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from app import create_app, db
import config


@pytest.fixture
def app():
    app = create_app(config.TestConfig)
    database_url = app.config.get("SQLALCHEMY_DATABASE_URI")
    engine = create_engine(database_url)
    if not database_exists(engine.url):
        create_database(engine.url)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        drop_database(database_url)


@pytest.fixture
def client(app):
    return app.test_client()
