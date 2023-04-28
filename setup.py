#!/usr/bin/env python3
from setuptools import setup, find_packages

required = [
    'sentry_sdk',
    'sentry-sdk[flask]',
    'blinker',
    "apispec",
    "PyYAML",
    "pymongo",
    "mongoengine",
    "Flask",
    "flask-cors",
    "flask-compress",
    "flask_mongoengine",
    "flask-smorest",
    "marshmallow",
    "marshmallow_enum",
    "colorlog",
    "gunicorn",
    "requests",
    "environs",
    "passlib",
    "healthcheck",
    "ping3"
]

VERSION = "2023.04.0"

setup(
      name='barbuc_api',
      version=VERSION,
      packages=find_packages(exclude=['tests', 'tests.*']),
      install_requires=required,
)
