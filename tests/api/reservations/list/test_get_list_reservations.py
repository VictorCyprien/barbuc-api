from flask.app import Flask
from rich import print

from unittest.mock import ANY

from barbuc_api.models.user import User
from barbuc_api.models.barbecue import Barbecue


def test_list_all_reservations_barbecue_admin(client: Flask, victor: User, tristan: User, member: User, toulouse: Barbecue, paris: Barbecue):
    data_login = {
        "email": victor.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    toulouse.user = tristan
    toulouse.save()
    paris.user = member
    paris.save()

    res = client.get("/api/barbecues/availables", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'reservations': [
            {
                '_date': '2023-04-27 18:30:00',
                'barbecue_id': ANY,
                'name': 'Mon Barbuc à Toulouse',
                'place': 'Toulouse',
                'user': {'name': 'Tristan CALVET', 'user_id': ANY}
            },
            {
                '_date': '2023-04-27 18:30:00',
                'barbecue_id': ANY,
                'name': 'Mon Barbuc à Paris',
                'place': 'Paris',
                'user': {'name': 'Member 1', 'user_id': ANY}
            }
        ]
    }


def test_list_all_reservations_barbecue_member(client: Flask, victor: User, tristan: User, member: User, toulouse: Barbecue, paris: Barbecue):
    data_login = {
        "email": member.email,
        "password": "beedemo"
    }

    res = client.post("/api/auth/login", json=data_login)
    token = res.json["token"]
    assert res.status_code == 201

    toulouse.user = tristan
    toulouse.save()
    paris.user = victor
    paris.save()

    res = client.get("/api/barbecues/availables", headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'reservations': []
    }


def test_list_all_reservations_barbecue_not_auth(client: Flask, victor: User, tristan: User, member: User, toulouse: Barbecue, paris: Barbecue):
    res = client.get("/api/barbecues/availables")
    assert res.status_code == 401
    data = res.json
    print(data)
    assert data == {
        'msg': 'Missing Authorization Header'
    }
