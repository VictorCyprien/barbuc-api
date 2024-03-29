import logging

from flask.views import MethodView
from flask_jwt_extended import create_access_token
from mongoengine.errors import DoesNotExist
from datetime import datetime
import pytz

from .auth_blp import auth_blp

from ...schemas.communs_schemas import PagingError
from ...schemas.auth_schemas import (
    LoginParamsSchema,
    LoginResponseSchema
)

from ...models.user import User
from ...helpers.errors_msg_handler import Unauthorized, ReasonError


logger = logging.getLogger('console')


@auth_blp.route('/login')
class LoginAuthView(MethodView):
    
    @auth_blp.doc(operationId='Login')
    @auth_blp.arguments(LoginParamsSchema)
    @auth_blp.response(401, schema=PagingError, description="Invalid credentials")
    @auth_blp.response(201, schema=LoginResponseSchema, description="Log the user")
    def post(self, user_login: dict):
        """Login the user"""
        logger.debug(f"Authenticate user with email: {user_login.get('email')}")
        email = user_login.get("email")
        password = user_login.get("password")
  
        if not User.isValidEmail(email):
            raise Unauthorized(ReasonError.BAD_CREDENTIALS.value)

        try:
            user: User = User.objects.get(email=email)
        except DoesNotExist as exc:
            logger.debug(f"Unauthenticated user: {exc}")
            raise Unauthorized(ReasonError.BAD_CREDENTIALS.value)
            
        if not user.check_password(password=password):
            raise Unauthorized(ReasonError.BAD_CREDENTIALS.value)
        
        token = create_access_token(identity=user.user_id)
        user.last_login = datetime.now(tz=pytz.utc).replace(microsecond=0)
        user.save()
        return {
            "msg": "Logged",
            "token": token
        }
