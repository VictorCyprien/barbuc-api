from flask.app import Flask
from rich import print
import datetime

from unittest.mock import ANY

from barbuc_api.models.user import User
from barbuc_api.models.barbecue import Barbecue


def test_create_barbecue(client: Flask, victor: User):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    data = {
        "name": "Mon Barbuc à Montauban",
        "place": "Montauban",
        "date": "2023-04-27 18:30:00"
    }

    res = client.post("/api/barbecues/", json=data, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 201
    data = res.json
    print(data)
    assert data == {
        'action': 'created',
        'barbecue': {
            '_date': '2023-04-27 18:30:00',
            'barbecue_id': ANY,
            'name': 'Mon Barbuc à Montauban',
            'place': 'Montauban'
        }
    }


    barbecue_id = data['barbecue']['barbecue_id']
    barbuc = Barbecue.objects().get(barbecue_id=barbecue_id)
    assert barbuc.name == 'Mon Barbuc à Montauban'
    assert barbuc.date == datetime.datetime(2023, 4, 27, 18, 30)

    barbuc.delete()


def test_create_barbecue_invalid_data(client: Flask, victor: User):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201


    data = {}

    res = client.post("/api/barbecues/", json=data, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 422
    data = res.json
    print(data)
    assert data == {
        'code': 422, 
        'errors': {
            'json': {
                'date': ['Missing data for required field.'],
                'name': ['Missing data for required field.'],
                'place': ['Missing data for required field.']
            }
        },
        'status': 'Unprocessable Entity'
    }


def test_barbecue_error_during_save(client: Flask, victor: User, mock_save_barbecue_document):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    data = {
        "name": "Mon Barbuc à Montauban",
        "place": "Montauban",
        "date": "2023-04-27 18:30:00"
    }

    res = client.post("/api/barbecues/", json=data, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 400
    data = res.json
    print(data)
    assert data == {
        'code': 400,
        'message': 'An error has occured during barbecue creation, please try again',
        'status': 'Bad Request'
    }

    mock_save_barbecue_document.assert_called()


def test_create_barbecue_not_admin(client: Flask, member: User):
    data_login = {
        "email": member.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    data = {
        "name": "Mon Barbuc à Montauban",
        "place": "Montauban",
        "date": "2023-04-27 18:30:00"
    }

    res = client.post("/api/barbecues/", json=data, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {
        'code': 401,
        'message': "You don't have the privileges to perform this action",
        'status': 'Unauthorized'
    }
