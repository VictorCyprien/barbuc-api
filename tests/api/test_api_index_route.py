from flask.app import Flask
from rich import print

from unittest.mock import ANY

from barbuc_api.models.user import User

def test_index_root(client_victor: Flask, victor: User):
    res = client_victor.get("/")
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'name': 'Barbuc-api'
    }
