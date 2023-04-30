from typing import Dict
import logging

from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import NotUniqueError, DoesNotExist

from .users_blp import users_blp
from .abstract_user_view import AbstractUsersView

from ...schemas.communs_schemas import PagingError
from ...schemas.users_schemas import (
    InputUpdateUserSchema,
    UserResponseSchema
)

from ...models.user import User
from ...helpers.errors_msg_handler import BadRequest, ReasonError, NotFound


logger = logging.getLogger('console')


@users_blp.route('/<int:user_id>')
class OneUserView(AbstractUsersView):

    @users_blp.doc(operationId='UpdateUser')
    @users_blp.arguments(InputUpdateUserSchema)
    @users_blp.response(400, schema=PagingError, description="BadRequest")
    @users_blp.response(404, schema=PagingError, description="NotFound")
    @users_blp.response(200, schema=UserResponseSchema, description="Update one user")
    @jwt_required()
    def put(self, input_dict: Dict, user_id: int):
        """Update an existing user"""
        auth_user = User.get_by_id(get_jwt_identity())
        
        if not self.can_read_the_user(
            auth_user_id=auth_user.user_id, 
            user_scopes=auth_user.scopes,
            user_id=user_id
        ):
            raise NotFound(f"User #{user_id} not found !")
        
        if input_dict.get("email", None) is not None and not User.isValidEmail(input_dict["email"]):
            raise BadRequest(ReasonError.INVALID_EMAIL.value)

        try:
            user = User.get_by_id(id=user_id)
        except DoesNotExist:
            raise NotFound(f"User #{user_id} not found !")

        user.update(input_dict)
        
        try:
            user.save()
        except NotUniqueError:
            raise BadRequest(ReasonError.UPDATE_USER_ERROR.value)

        return {
            "action": "updated",
            "user": user
        }


    @users_blp.doc(operationId='DeleteUser')
    @users_blp.response(400, schema=PagingError, description="BadRequest")
    @users_blp.response(404, schema=PagingError, description="NotFound")
    @users_blp.response(200, schema=UserResponseSchema, description="Delete one user")
    @jwt_required()
    def delete(self, user_id: int):
        """Delete an existing user"""
        auth_user = User.get_by_id(get_jwt_identity())
        
        if not self.can_read_the_user(
            auth_user_id=auth_user.user_id, 
            user_scopes=auth_user.scopes,
            user_id=user_id
        ):
            raise NotFound(f"User #{user_id} not found !")

        user = User.get_by_id(id=user_id)
        user.delete()

        return {
            "action": "deleted",
            "user": user
        }
