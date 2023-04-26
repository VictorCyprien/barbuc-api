import json
import sys
import logging.config
import click
from environs import Env

from urllib.parse import urlparse

from flask import Flask, request, jsonify
from flask_compress import Compress
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_smorest import Api
from flask.cli import AppGroup
from flask_wtf.csrf import CSRFProtect

from flask_jwt_extended import JWTManager

import redis

from mongoengine import errors

from healthcheck import HealthCheck

from .config import Config
from ..helpers.check_mongodb import get_mongodb_status


def create_flask_app(config: Config) -> Flask:
    # Create the Flask App
    app = Flask(__name__)

    # Set config env
    app.config["WTF_CSRF_CHECK_DEFAULT"] = True
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config["JWT_SECRET_KEY"] = config.FLASK_JWT
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_ACCESS_TOKEN_EXPIRES

    # Set token auth and redis blacklist
    jwt = JWTManager(app)

    jwt_redis_blocklist = redis.StrictRedis(
        host="localhost", port=6379, db=0, decode_responses=True
    )

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token_in_redis = jwt_redis_blocklist.get(jti)
        return token_in_redis is not None

    @jwt.expired_token_loader
    def my_expired_token_callback(jwt_header, jwt_payload):
        return jsonify(code=401, message="Token expired", status="Unauthorized"), 401

    @jwt.unauthorized_loader
    def my_missing_token_callback(callback):
        return jsonify(code=401, message="Not Authenticated", status="Unauthorized"), 401
    
    @jwt.invalid_token_loader
    def my_invalid_token(callback):
        return jsonify(code=401, message="Invalid token", status="Unauthorized"), 401
    
    @jwt.revoked_token_loader
    def my_missing_token_callback(jwt_header, jwt_payload):
        return jsonify(code=401, message="Not Authenticated", status="Unauthorized"), 401
    

    app.extensions['jwt_redis_blocklist'] = jwt_redis_blocklist

    # csrf = CSRFProtect()
    # csrf.init_app(app)

    CORS(app, resources={r"/foo": {"origins": "https://localhost:port"}})
    Compress(app)

    app.logger = logging.getLogger('console')

    """ Log each API/APP request
    """

    @app.before_request
    def before_request():
        """ Log every requests """
        app.logger.info(f'>-- {request.method} {request.path} from {request.remote_addr}')
        app.logger.debug(f'       Args: {request.args.to_dict()}')
        app.logger.debug(f'    Headers: {request.headers.to_wsgi_list()}')
        app.logger.debug(f'       Body: {request.get_data()}')

    @app.after_request
    def after_request(response):
        """ Log response status, after every request. """
        app.logger.info(f'--> Response status: {response.status}')
        app.logger.debug(f'      Body: {response.json}')
        return response

    env = Env()

    app.logger.info('.------------------.')
    app.logger.info('|    Barbuc-api    |')
    app.logger.info('.------------------.')

    # Update config from given one
    app.config.update(**config.json)

    app.logger.info(f"Config: {json.dumps(config.json, indent=4)}")

    # Log the current conf
    cname = env.str('CI_COMMIT_REF_NAME', None)
    csha = env.str('CI_COMMIT_SHA', None)
    if cname:
        app.logger.info(f"Current commit name: {cname}")
    if csha:
        app.logger.info(f"Current commit sha: {csha}")

    app.debug = config.FLASK_ENV

    # Configure mongo client
    app.mongo_client = MongoEngine(app=app)

    #Add healthcheck
    health = HealthCheck(app, "/healthcheck")
    health.add_check(get_mongodb_status(app.mongo_client))

    @app.route('/')
    def index():
        res = {
            'name': config.SERVICE_NAME,
            'commit_name': cname,
            'commit_sha': csha,
        }
        return jsonify(res)   

    rest_api = Api(app)
    
    from .views.users import users_blp
    rest_api.register_blueprint(users_blp)

    from .views.auth import auth_blp
    rest_api.register_blueprint(auth_blp)

    app.logger.debug(f"URL Map: \n{app.url_map}")
    return app
