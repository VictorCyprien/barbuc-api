from flask.app import Flask
from rich import print

from unittest.mock import ANY

from barbuc_api.models.user import User

def test_healthcheck_root(client_victor: Flask, victor: User):
    res = client_victor.get("/healthcheck")
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'hostname': ANY,
        'status': 'success',
        'timestamp': ANY,
        'results': [
            {
                'checker': 'mongo',
                'output': 'Database is ok',
                'passed': True,
                'timestamp': ANY,
                'expires': ANY
            },
            {
                'checker': 'redis',
                'output': 'Redis cache server is ok',
                'passed': True,
                'timestamp': ANY,
                'expires': ANY
            }
        ]
    }
