from flask.app import Flask
import freezegun
from barbuc_api.helpers.errors_msg_handler import ReasonError
from rich import print

from unittest.mock import ANY

from barbuc_api.models.user import User


def test_login_user(app, client_victor: Flask, victor: User):

    data = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client_victor.post("/api/auth/login", json=data)
    data = res.json
    print(data)
    assert data == {
        'msg': 'Logged',
        'token': ANY
    }


def test_login_user_wrong_credentials(app, client_victor: Flask, victor: User):

    data = {
        "email": victor.email,
        "password": "123"
    }

    res = client_victor.post("/api/auth/login", json=data)
    data = res.json
    print(data)
    assert data == {
        'code': 401,
        'message': 'The email or password is incorrect',
        'status': 'Unauthorized'
    }


def test_login_user_invalid_email(app, client_victor: Flask, victor: User):

    data = {
        "email": "123",
        "password": "beedemo"
    }

    res = client_victor.post("/api/auth/login", json=data)
    data = res.json
    print(data)
    assert data == {
        'code': 401, 
        'message': 'The email or password is incorrect', 
        'status': 'Unauthorized'
    }


def test_login_user_not_found(app, client_victor: Flask, victor: User):

    data = {
        "email": "test.test@test.fr",
        "password": "beedemo"
    }

    res = client_victor.post("/api/auth/login", json=data)
    data = res.json
    print(data)
    assert data == {
        'code': 401,
        'message': 'The email or password is incorrect',
        'status': 'Unauthorized'
    }
