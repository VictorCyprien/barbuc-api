from mongoengine.connection import get_db, get_connection
import pymongo
from typing import TYPE_CHECKING, Union, Callable
import logging

from ..config import config
from ..models.user import User

default_logger: logging.Logger = logging.getLogger("console")

def mongo_available():
    def check():
        conn = User.objects().first()
        assert isinstance(conn, User)
        return True, "Database is ok"
    check.__name__ = "mongo"
    return check
