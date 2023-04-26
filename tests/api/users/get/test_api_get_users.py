from flask.app import Flask
from rich import print

from unittest.mock import ANY

from barbuc_api.models.user import User

def test_get_users(client: Flask, victor: User, tristan: User):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    res = client.get("/api/users/", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'users': [
            {
                '_creation_time': '2000-01-01 00:00:00',
                '_last_login': ANY,
                '_update_time': '2000-01-01 00:00:00',
                'email': 'victor.cyprien@barbuc.fr',
                'name': 'Victor CYPRIEN',
                'user_id': ANY
            },
            {
                '_creation_time': '2000-01-01 00:00:00',
                '_last_login': ANY,
                '_update_time': '2000-01-01 00:00:00',
                'email': 'tristan.calvet@barbuc.fr',
                'name': 'Tristan CALVET',
                'user_id': ANY
            }
        ]
    }


def test_get_users_not_auth(client: Flask, victor: User, tristan: User):
    res = client.get("/api/users/")
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {'msg': 'Missing Authorization Header'}