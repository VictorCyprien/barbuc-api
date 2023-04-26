from flask.app import Flask
import freezegun
from barbuc_api.helpers.errors_msg_handler import ReasonError
from rich import print

from flask_jwt_extended import create_access_token

from unittest.mock import ANY

from barbuc_api.models.user import User


def test_create_user(client_victor: Flask, victor: User):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client_victor.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    data = {
        "email": "test.test@test.fr",
        "password": "beedemo",
        "name": "TestUser"
    }

    res = client_victor.post("/api/users/", json=data, headers={'Authorization': f'Bearer {token}'})
    #assert res.status_code == 201
    data = res.json
    print(data)
    assert data == {}