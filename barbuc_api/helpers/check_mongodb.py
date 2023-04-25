from pymongo import MongoClient
from typing import TYPE_CHECKING, Union, Callable
import logging


if TYPE_CHECKING:
    from pymongo import MongoClient
    from flask_mongoengine import MongoEngine

default_logger: logging.Logger = logging.getLogger("console")


def monitor_mongodb_status(mongodb_cnx: 'Union[MongoClient, Callable[[], MongoClient]]', logger: logging.Logger = None):
    if logger is None:
        logger = default_logger
    def mongodb_status():
        is_database_working = True
        output = 'database is ok'
        _mongodb_cnx = mongodb_cnx if not callable(mongodb_cnx) else mongodb_cnx()
        try:
            # to check database we will execute raw query
            v = _mongodb_cnx.server_info()
        except Exception as e:
            logger.exception('Issue while testing MongoDB')
            logger.error(e)
            output = str(e)
            is_database_working = False
        return is_database_working, output
    return mongodb_status


def get_mongodb_status(flask_mongoengine_client: 'MongoEngine'):
    mongo_cnx = lambda: flask_mongoengine_client.connection
    return monitor_mongodb_status(mongo_cnx, logger=default_logger)

