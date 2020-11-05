import pytest

from expedition_merman_wrapper import create_app, db


@pytest.fixture('module')
def app():
    _app = create_app('testing', config_name='test')

    with _app.app_context():
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()


@pytest.fixture('module')
def session(app):
    session = db.session(autoflush=False)

    return session
