import pytest

from app import app, db

im_app=app

@pytest.fixture()
def app():
    app=im_app
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()

    yield app
    db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()
