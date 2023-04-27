from flask.app import Flask
from rich import print
import datetime

from unittest.mock import ANY

from mongoengine.errors import ValidationError

from barbuc_api.models.user import User
from barbuc_api.models.barbucue import Barbucue


def test_create_barbucue(client: Flask, victor: User):
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

    res = client.post("/api/barbucues/", json=data, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 201
    data = res.json
    print(data)
    assert data == {
        'action': 'created',
        'barbucue': {
            '_date': '2023-04-27 18:30:00',
            'barbuc_id': ANY,
            'name': 'Mon Barbuc à Montauban',
            'place': 'Montauban'
        }
    }


    barbuc_id = data['barbucue']['barbuc_id']
    barbuc = Barbucue.objects().get(barbuc_id=barbuc_id)
    assert barbuc.name == 'Mon Barbuc à Montauban'
    assert barbuc.date == datetime.datetime(2023, 4, 27, 18, 30)

    barbuc.delete()


def test_create_barbucue_invalid_data(client: Flask, victor: User):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201


    data = {}

    res = client.post("/api/barbucues/", json=data, headers={'Authorization': f'Bearer {token}'})
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


def test_barbucue_error_during_save(client: Flask, victor: User, mock_save_barbucue_document):
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

    res = client.post("/api/barbucues/", json=data, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 400
    data = res.json
    print(data)
    assert data == {
        'code': 400,
        'message': 'An error has occured during barbucue creation, please try again',
        'status': 'Bad Request'
    }

    mock_save_barbucue_document.assert_called()


def test_create_barbucue_not_admin(client: Flask, member: User):
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

    res = client.post("/api/barbucues/", json=data, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {
        'code': 401,
        'message': "You don't have the privileges to perform this action",
        'status': 'Unauthorized'
    }
