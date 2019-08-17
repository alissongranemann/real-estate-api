import pytest

from app import create_app
from config import TestConfig


@pytest.fixture(scope="session")
def app(request):
    app = create_app(TestConfig())
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def db(app, request):
    """Session-wide test database."""
    from flasky import db

    def teardown():
        db.session.close()
        db.drop_all()

    db.app = app
    db.create_all()

    request.addfinalizer(teardown)
    return db


@pytest.fixture(scope="function")
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
