import pytest

from app import create_app, db


@pytest.fixture()
def prepare_app_context():
    app = create_app('test')
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()
    app_context.pop()

