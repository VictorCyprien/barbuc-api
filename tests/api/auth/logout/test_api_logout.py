from flask.app import Flask
from rich import print

from barbuc_api.models.user import User


def test_logout_user(client_victor: Flask, victor: User):
    data = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client_victor.post("/api/auth/login", json=data)
    token = res.json["token"]
    assert res.status_code == 201

    res = client_victor.post("/api/auth/logout", headers={'Authorization': f'Bearer {token}'})
    data = res.json
    print(data)
    assert data == {
        'msg': 'You have been logout !'
    }


def test_logout_user_not_logged(client_victor: Flask, victor: User):
    res = client_victor.post("/api/auth/logout")
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {
        'msg': 'Missing Authorization Header'
    }
