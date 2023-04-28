from flask.app import Flask
from rich import print

from unittest.mock import ANY

from barbuc_api.models.user import User
from barbuc_api.models.barbecue import Barbecue

def test_check_barbecue_available(client: Flask, victor: User, toulouse: Barbecue):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    res = client.get(f"/api/barbecues/{toulouse.barbecue_id}/available", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'is_available': True
    }


def test_barbecue_not_available(client: Flask, victor: User, toulouse: Barbecue):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    toulouse.user = victor
    toulouse.save()

    res = client.get(f"/api/barbecues/{toulouse.barbecue_id}/available", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'is_available': False
    }


def test_check_barbecue_available_not_auth(client: Flask, victor: User, toulouse: Barbecue):

    res = client.get(f"/api/barbecues/{toulouse.barbecue_id}/available")
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {
        'msg': 'Missing Authorization Header'
    }
