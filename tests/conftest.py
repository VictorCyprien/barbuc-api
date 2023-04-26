from datetime import datetime

from werkzeug.datastructures import Headers

from mongoengine.connection import disconnect

from flask import Flask
from flask import testing
from flask.testing import FlaskClient
from flask import current_app
import jwt

from unittest.mock import Mock
import pytest
from rich import print
import freezegun

from barbuc_api.app.models import User
from barbuc_api.config import config


@pytest.fixture(scope='session')
def app(request) -> Flask:
    """ Session-wide test `Flask` application. """
    disconnect()    # force close potential existing mongo connection
    from barbuc_api.config import config
    config.MONGODB_URI = "mongomock://localhost"
    config.MONGODB_DATABASE = "test"
    config.MONGODB_CONNECT = False


    from barbuc_api.app import create_flask_app
    _app = create_flask_app(config=config)
    yield _app


class TestClient(testing.FlaskClient):
    global_headers = {}
    def open(self, *args, **kwargs):
        api_key_headers = Headers(self.global_headers)
        headers = kwargs.pop('headers', {})
        if not isinstance(headers, Headers):
            headers = Headers(headers)
        headers.extend(api_key_headers)
        kwargs['headers'] = headers
        return super().open(*args, **kwargs)


@pytest.fixture(scope='module')
def client(app: Flask) -> TestClient:
    app.test_client_class = TestClient
    client = app.test_client()
    yield client


def _set_user_auth_headers(client: TestClient, user: User) -> FlaskClient:
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': user.user_id
    }
    token = jwt.encode(
        payload,
        123456,
        algorithm='HS256'
    )

    client.global_headers = {'Authorization': f'Bearer {token.decode()}'}
    return client


def _raz_auth_headers(client: TestClient):
    client.global_headers = {}


@pytest.fixture(scope='function')
def client_victor(client: TestClient, victor: User) -> FlaskClient:
    _set_user_auth_headers(client, victor)
    yield client
    _raz_auth_headers(client)


@pytest.fixture(scope='function')
def client_tristan(client: TestClient, tristan: User) -> FlaskClient:
    _set_user_auth_headers(client, tristan)
    yield client
    _raz_auth_headers(client)


@pytest.fixture(scope='function')
def client_member(client: TestClient, member: User) -> FlaskClient:
    _set_user_auth_headers(client, member)
    yield client
    _raz_auth_headers(client)



@pytest.fixture(scope='function')
def victor(app) -> User:
    #  victor is "superadmin"
    user_dict = {
        "email": "victor.cyprien@barbuc.fr",
        "name": "Victor CYPRIEN",
        "password": "beedemo"
    }
    with freezegun.freeze_time('2000-01-01T00:00:00+00:00'):
        user = User.create(user_dict)
        user.scopes = ["user:admin"]
        user.save()
    yield user
    user.delete()


@pytest.fixture(scope='function')
def tristan(app) -> User:
    #  tristan is "superadmin"
    user_dict = {
        "email": "tristan.calvet@barbuc.fr",
        "name": "Tristan CALVET",
        "password": "beedemo"
    }
    with freezegun.freeze_time('2000-01-01T00:00:00+00:00'):
        user = User.create(user_dict)
        user.scopes = ["user:admin"]
        user.save()
    yield user
    user.delete()


@pytest.fixture(scope='function')
def member(app) -> User:
    #  member is not "superadmin"
    user_dict = {
        "email": "member1@barbuc.fr",
        "name": "Member 1",
        "password": "beedemo"
    }
    with freezegun.freeze_time('2000-01-01T00:00:00+00:00'):
        user = User.create(user_dict)
        user.save()
    yield user
    user.delete()

