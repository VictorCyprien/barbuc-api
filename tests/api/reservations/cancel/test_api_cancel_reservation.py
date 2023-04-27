from flask.app import Flask
from rich import print

from unittest.mock import ANY

from barbuc_api.models.user import User
from barbuc_api.models.barbecue import Barbecue

def test_cancel_reservation_barbecue(client: Flask, victor: User, toulouse: Barbecue):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    toulouse.user = victor
    toulouse.save()

    res = client.post(f"/api/barbecues/{toulouse.barbecue_id}/cancel", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 201
    data = res.json
    print(data)
    assert data == {
        'action': 'canceled',
        'barbecue': {
            '_date': '2023-04-27 18:30:00',
            'barbecue_id': ANY,
            'name': 'Mon Barbuc à Toulouse',
            'place': 'Toulouse'
        },
        'user': {
            '_creation_time': '2000-01-01 00:00:00',
            '_last_login': ANY,
            '_update_time': '2000-01-01 00:00:00',
            'email': 'victor.cyprien@barbuc.fr',
            'name': 'Victor CYPRIEN',
            'user_id': ANY
        }
    }


def test_cancel_reservation_barbecue_differents_users(client: Flask, victor: User, tristan: User, toulouse: Barbecue):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    toulouse.user = tristan
    toulouse.save()

    res = client.post(f"/api/barbecues/{toulouse.barbecue_id}/cancel", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {
        'code': 401,
        'message': 'This barbecue is reserved by someone else',
        'status': 'Unauthorized'
    }


def test_calcel_reservation_barbecue_not_auth(client: Flask, victor: User, toulouse: Barbecue):
    res = client.post(f"/api/barbecues/{toulouse.barbecue_id}/cancel")
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {
        'msg': 'Missing Authorization Header'
    }


def test_cancel_reservation_barbecue_not_found(client: Flask, victor: User, toulouse: Barbecue):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    toulouse.user = victor
    toulouse.save()

    res = client.post("/api/barbecues/1234/cancel", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 404
    data = res.json
    print(data)
    assert data == {
        'code': 404, 
        'message': 'Barbecue #1234 not found !', 
        'status': 'Not Found'
    }



def test_cancel_not_reserved_barbecue(client: Flask, victor: User, toulouse: Barbecue):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    res = client.post(f"/api/barbecues/{toulouse.barbecue_id}/cancel", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {
        'code': 401,
        'message': 'This barbecue is not reserved',
        'status': 'Unauthorized'
    }


def test_cancel_reservation_barbecue_save_error(client: Flask, victor: User, dijon: Barbecue, mock_save_barbecue_document):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    res = client.post(f"/api/barbecues/{dijon.barbecue_id}/cancel", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 400
    data = res.json
    print(data)
    assert data == {
        'code': 400,
        'message': 'An error has occured during barbecue update, please try again',
        'status': 'Bad Request'
    }

    mock_save_barbecue_document.assert_called()
