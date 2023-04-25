import logging

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from mongoengine.errors import NotUniqueError, ValidationError

from .users_blp import users_blp

from ...schemas.users_schemas import (
    InputCreateUserSchema,
    UserResponseSchema,
    GetUsersListSchema
)

from ...models.user import User
from ....helpers.errors_msg_handler import BadRequest, ReasonError


logger = logging.getLogger('console')


@users_blp.route('/')
class RootUsersView(MethodView):

    @users_blp.doc(operationId='ListUsers')
    @users_blp.response(200, schema=GetUsersListSchema, description="List of users found in the database")
    @jwt_required()
    def get(self):
        """Retrieve list of users"""
        users = User.objects()

        return {
            'users': users,
        }


    @users_blp.doc(operationId='CreateUser')
    @users_blp.arguments(InputCreateUserSchema)
    @users_blp.response(201, schema=UserResponseSchema, description="Infos of new user")
    @jwt_required()
    def post(self, input_data: dict):
        """Create a new user"""
        if not User.isValidEmail(input_data["email"]):
            raise BadRequest(ReasonError.INVALID_EMAIL.value)
        user = User.create(input_data=input_data)

        try:
            user.save()
        except ValidationError:
            raise BadRequest(ReasonError.UPDATE_USER_ERROR.value)
        except NotUniqueError:
            raise BadRequest(ReasonError.EMAIL_ALREADY_USED.value)

        return {
            'action': 'created',
            'user': user
        }
