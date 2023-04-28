from flask.app import Flask
from rich import print

from unittest.mock import ANY

from barbuc_api.models.user import User
from barbuc_api.models.barbecue import Barbecue

def test_barbecue_update(client: Flask, victor: User, paris: Barbecue):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    data_put = {
        "name": "Mon autre barbuc à Paris",
        "place": "Toujours à Paris",
        "date": "2023-05-15 12:45:00"
    }

    res = client.put(f"/api/barbecues/{paris.barbecue_id}", json=data_put, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'action': 'updated',
        'barbecue': {
            '_date': '2023-05-15 12:45:00',
            'barbecue_id': ANY,
            'name': 'Mon autre barbuc à Paris',
            'place': 'Toujours à Paris'
        }
    }


def test_barbecue_update_not_auth(client: Flask, paris: Barbecue):
    data_put = {
        "name": "Mon autre barbuc à Paris illégal",
    }

    res = client.put(f"/api/barbecues/{paris.barbecue_id}", json=data_put)
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {'msg': 'Missing Authorization Header'}


def test_barbecue_update_not_admin(client: Flask, member: User, paris: Barbecue):
    data_login = {
        "email": member.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    data_put = {
        "name": "Mon autre barbuc à Paris",
    }

    res = client.put(f"/api/barbecues/{paris.barbecue_id}", json=data_put, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 404
    data = res.json
    print(data)
    assert data == {
        'code': 404, 
        'message': f'Barbecue #{paris.barbecue_id} not found !', 
        'status': 'Not Found'
    }

def test_barbecue_error_during_update(client: Flask, victor: User, toulouse: Barbecue, mock_save_barbecue_document):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    data_put = {
        "name": "Erreur"
    }

    res = client.put(f"/api/barbecues/{toulouse.barbecue_id}", json=data_put, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 400
    data = res.json
    print(data)
    assert data == {
        'code': 400,
        'message': 'An error has occured during barbecue update, please try again',
        'status': 'Bad Request'
    }

    mock_save_barbecue_document.assert_called()
