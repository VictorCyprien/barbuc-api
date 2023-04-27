from flask.app import Flask
from rich import print

from unittest.mock import ANY

from barbuc_api.models.user import User
from barbuc_api.models.barbecue import Barbecue

def test_delete_barbecue(client: Flask, victor: User, toulouse: Barbecue):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    res = client.delete(f"/api/barbecues/{toulouse.barbecue_id}", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'action': 'deleted',
        'barbecue': {
            '_date': '2023-04-27 18:30:00',
            'barbecue_id': ANY,
            'name': 'Mon Barbuc à Toulouse',
            'place': 'Toulouse'
        }
    }


def test_delete_barbecue_not_auth(client: Flask, victor: User, toulouse: Barbecue):
    res = client.delete(f"/api/barbecues/{toulouse.barbecue_id}")
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {'msg': 'Missing Authorization Header'}


def test_delete_barbecue_not_admin(client: Flask, member: User, toulouse: Barbecue):
    data_login = {
        "email": member.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    res = client.delete(f"/api/barbecues/{toulouse.barbecue_id}", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 404
    data = res.json
    print(data)
    assert data == {
        'code': 404, 
        'message': f'Barbecue #{toulouse.barbecue_id} not found !', 
        'status': 'Not Found'
    }
