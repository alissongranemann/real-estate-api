import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from app import create_app
import config


@pytest.fixture(scope="session")
def app():
    app = create_app(config.TestConfig)

    database_url = app.config.get("SQLALCHEMY_DATABASE_URI")
    engine = create_engine(database_url)
    if not database_exists(engine.url):
        create_database(engine.url)

    yield app

    drop_database(database_url)


@pytest.fixture(scope="function")
def db(app, request):
    from app import db

    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app, db):
    return app.test_client()
