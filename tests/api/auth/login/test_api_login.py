from flask.app import Flask
import freezegun
from barbuc_api.helpers.errors_msg_handler import ReasonError
from rich import print

from unittest.mock import ANY

from barbuc_api.app.models.user import User


def test_login_user(client_victor: Flask, victor: User):

    res = client_victor.post("/api/login")
    print(res)
    assert res == {}
