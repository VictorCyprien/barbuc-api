from flask.app import Flask
from rich import print

from unittest.mock import ANY

from mongoengine.errors import ValidationError

from barbuc_api.models.user import User


def test_create_user(client: Flask, victor: User):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    data = {
        "email": "test.test@test.fr",
        "password": "beedemo",
        "name": "TestUser"
    }

    res = client.post("/api/users/", json=data, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 201
    data = res.json
    print(data)
    assert data == {
        'action': 'created',
        'user': {
            '_creation_time': ANY,
            '_last_login': ANY,
            '_update_time': ANY,
            'email': 'test.test@test.fr',
            'name': 'TestUser',
            'user_id': ANY
        }
    }

    user_id = data['user']['user_id']
    user = User.objects().get(user_id=user_id)
    assert user.email == 'test.test@test.fr'
    assert user._password.startswith("$pbkdf2-sha256$")

    user.delete()


def test_create_user_already_exist(client: Flask, victor: User):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201


    data = {
        "email": "test.test@test.fr",
        "password": "beedemo",
        "name": "TestUser"
    }

    user_already_created = User.create(data)
    user_already_created.save()
    user_already_created.reload()

    new_data = {
        "email": "test.test@test.fr",
        "password": "beedemo",
        "name": "TestUser"
    }

    res = client.post("/api/users/", json=new_data, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 400
    data = res.json
    print(data)
    assert data == {
        'code': 400, 
        'message': 'Unable to create this user, the email address is already in use', 
        'status': 'Bad Request'
    }

    user_already_created.delete()


def test_create_user_invalid_data(client: Flask, victor: User):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201


    data = {}

    res = client.post("/api/users/", json=data, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 422
    data = res.json
    print(data)
    assert data == {
        'code': 422, 
        'errors': {
            'json': {
                'email': ['Missing data for required field.'], 
                'name': ['Missing data for required field.'], 
                'password': ['Missing data for required field.']
            }
        },
        'status': 'Unprocessable Entity'
    }


def test_create_user_invalid_email(client: Flask, victor: User):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    data = {
        "email": "blabla",
        "password": "beedemo",
        "name": "TestUser"
    }

    res = client.post("/api/users/", json=data, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 400
    data = res.json
    print(data)
    assert data == {
        'code': 400, 
        'message': 'This email is invalid', 
        'status': 'Bad Request'
    }


def test_create_user_email_already_used(client: Flask, victor: User):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    data = {
        "email": "blabla",
        "password": "beedemo",
        "name": "TestUser"
    }

    res = client.post("/api/users/", json=data, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 400
    data = res.json
    print(data)
    assert data == {
        'code': 400, 
        'message': 'This email is invalid', 
        'status': 'Bad Request'
    }

def test_user_error_during_save(client: Flask, victor: User, mock_save_user_document):
    mock_save_user_document.side_effect = None
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    data = {
        "email": "test.test@test.fr",
        "password": "beedemo",
        "name": "TestUser"
    }

    mock_save_user_document.side_effect = ValidationError

    res = client.post("/api/users/", json=data, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 400
    data = res.json
    print(data)
    assert data == {
        'code': 400,
        'message': 'An error has occured during profil creation, please try again',
        'status': 'Bad Request'
    }

    mock_save_user_document.assert_called()
