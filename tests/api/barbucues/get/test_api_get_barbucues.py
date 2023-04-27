from flask.app import Flask
from rich import print

from unittest.mock import ANY

from barbuc_api.models.user import User
from barbuc_api.models.barbucue import Barbucue

def test_get_barbucues(client: Flask, victor: User, toulouse: Barbucue, paris: Barbucue):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    res = client.get("/api/barbucues/", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'barbucues': [
            {
                '_date': '2023-04-27 18:30:00',
                'barbuc_id': ANY,
                'name': 'Mon Barbuc à Toulouse',
                'place': 'Toulouse'
            },
            {
                '_date': '2023-04-27 18:30:00',
                'barbuc_id': ANY,
                'name': 'Mon Barbuc à Paris',
                'place': 'Paris'
            }
        ]
    }


def test_get_barbucues_not_auth(client: Flask, victor: User, tristan: User):
    res = client.get("/api/barbucues/")
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {'msg': 'Missing Authorization Header'}


def test_get_barbucues_not_admin(client: Flask, member: User):
    data_login = {
        "email": member.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    res = client.get("/api/barbucues/", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {
        'code': 401,
        'message': "You don't have the privileges to perform this action",
        'status': 'Unauthorized'
    }
