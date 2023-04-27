from typing import Union, Callable
import logging
import redis

default_logger: logging.Logger = logging.getLogger("console")

def redis_available(client_redis):
    def check():
        client_redis.info()
        return True, "Redis cache server is ok"
    check.__name__ = "redis"
    return check
