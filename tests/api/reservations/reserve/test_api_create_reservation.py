from flask.app import Flask
from rich import print

from unittest.mock import ANY

from barbuc_api.models.user import User
from barbuc_api.models.barbecue import Barbecue

def test_reserve_barbecue(client: Flask, victor: User, toulouse: Barbecue):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    res = client.post(f"/api/barbecues/{toulouse.barbecue_id}/reserve", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 201
    data = res.json
    print(data)
    assert data == {
        'action': 'reserved',
        'barbecue': {
            '_date': '2023-04-27 18:30:00',
            'barbecue_id': ANY,
            'name': 'Mon Barbuc à Toulouse',
            'place': 'Toulouse',
            'user': {
                'name': 'Victor CYPRIEN', 
                'user_id': ANY
            }
        }
    }


def test_reserve_barbecue_when_already_reserved(client: Flask, victor: User, tristan: User, toulouse: Barbecue):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    toulouse.user = tristan
    toulouse.save()

    res = client.post(f"/api/barbecues/{toulouse.barbecue_id}/reserve", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {
        'code': 401,
        'message': 'This barbecue is already reserved',
        'status': 'Unauthorized'
    }


def test_reserve_barbecue_not_auth(client: Flask, victor: User, toulouse: Barbecue):
    res = client.post(f"/api/barbecues/{toulouse.barbecue_id}/reserve")
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {
        'msg': 'Missing Authorization Header'
    }


def test_reserve_barbecue_save_error(client: Flask, victor: User, toulouse: Barbecue, mock_save_barbecue_document):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    res = client.post(f"/api/barbecues/{toulouse.barbecue_id}/reserve", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 400
    data = res.json
    print(data)
    assert data == {
        'code': 400,
        'message': 'An error has occured during barbecue update, please try again',
        'status': 'Bad Request'
    }
