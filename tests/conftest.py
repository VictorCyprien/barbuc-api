
from typing import Iterator
from flask import Flask
from flask import testing
from flask.testing import FlaskClient
from flask_jwt_extended import JWTManager

from werkzeug.datastructures import Headers

from mongoengine.connection import disconnect
from unittest.mock import Mock
import pytest
import freezegun

from barbuc_api.models.user import User
from barbuc_api.models.barbecue import Barbecue


@pytest.fixture(scope='session')
def app(request) -> Iterator[Flask]:
    """ Session-wide test `Flask` application. """
    disconnect()    # force close potential existing mongo connection
    from barbuc_api.config import config
    config.MONGODB_URI = "mongomock://localhost"
    config.MONGODB_DATABASE = "test"
    config.MONGODB_CONNECT = False

    config.SECURITY_PASSWORD_SALT = "123456"
    config.FLASK_JWT = "123456"
    config.JWT_ACCESS_TOKEN_EXPIRES = 7200

    from barbuc_api.app import create_flask_app
    _app = create_flask_app(config=config)
    JWTManager(_app)
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
def client(app: Flask) -> Iterator[TestClient]:
    app.test_client_class = TestClient
    client = app.test_client()
    yield client


def _raz_auth_headers(client: TestClient):
    client.global_headers = {}


@pytest.fixture(scope='function')
def client_victor(client: TestClient, victor: User) -> Iterator[FlaskClient]:
    yield client
    _raz_auth_headers(client)


@pytest.fixture(scope='function')
def client_tristan(client: TestClient, tristan: User) -> Iterator[FlaskClient]:
    yield client
    _raz_auth_headers(client)


@pytest.fixture(scope='function')
def client_member(client: TestClient, member: User) -> Iterator[FlaskClient]:
    yield client
    _raz_auth_headers(client)


#### USERS ####

creation_date = '2000-01-01T00:00:00+00:00'

@pytest.fixture(scope='function')
def victor(app) -> Iterator[User]:
    #  victor is "superadmin"
    user_dict = {
        "email": "victor.cyprien@barbuc.fr",
        "name": "Victor CYPRIEN",
        "password": "beedemo"
    }
    with freezegun.freeze_time(creation_date):
        user = User.create(user_dict)
        user.scopes = ["user:admin"]
        user.save()
    yield user
    user.delete()


@pytest.fixture(scope='function')
def tristan(app) -> Iterator[User]:
    #  tristan is "superadmin"
    user_dict = {
        "email": "tristan.calvet@barbuc.fr",
        "name": "Tristan CALVET",
        "password": "beedemo"
    }
    with freezegun.freeze_time(creation_date):
        user = User.create(user_dict)
        user.scopes = ["user:admin"]
        user.save()
    yield user
    user.delete()


@pytest.fixture(scope='function')
def member(app) -> Iterator[User]:
    #  member is not "superadmin"
    user_dict = {
        "email": "member1@barbuc.fr",
        "name": "Member 1",
        "password": "beedemo"
    }
    with freezegun.freeze_time(creation_date):
        user = User.create(user_dict)
        user.save()
    yield user
    user.delete()


#### BARBECUES ####

date_place = "2023-04-27 18:30:00"

@pytest.fixture(scope='function')
def toulouse(app) -> Iterator[Barbecue]:
    barbuc_dict = {
        "name": "Mon Barbuc à Toulouse",
        "place": "Toulouse",
        "date": date_place
    }
    with freezegun.freeze_time(creation_date):
        barbecue = Barbecue.create(barbuc_dict)
        barbecue.save()
    yield barbecue
    barbecue.delete()


@pytest.fixture(scope='function')
def paris(app) -> Iterator[Barbecue]:
    barbuc_dict = {
        "name": "Mon Barbuc à Paris",
        "place": "Paris",
        "date": date_place
    }
    with freezegun.freeze_time(creation_date):
        barbecue = Barbecue.create(barbuc_dict)
        barbecue.save()
    yield barbecue
    barbecue.delete()

@pytest.fixture(scope='function')
def dijon(app, victor) -> Iterator[Barbecue]:
    barbuc_dict = {
        "name": "Mon Barbuc à Dijon",
        "place": "Dijon",
        "date": date_place
    }
    with freezegun.freeze_time(creation_date):
        barbecue = Barbecue.create(barbuc_dict)
        barbecue.user = victor
        barbecue.save()
    yield barbecue
    barbecue.delete()


#### MOCKS ####

@pytest.fixture
def mock_save_user_document():
    from barbuc_api.models.user import User
    from mongoengine.errors import ValidationError
    _original = User.save
    User.save = Mock()
    User.save.side_effect = ValidationError
    yield User.save
    User.save = _original


@pytest.fixture
def mock_save_barbecue_document():
    from barbuc_api.models.barbecue import Barbecue
    from mongoengine.errors import ValidationError
    _original = Barbecue.save
    Barbecue.save = Mock()
    Barbecue.save.side_effect = ValidationError
    yield Barbecue.save
    Barbecue.save = _original
