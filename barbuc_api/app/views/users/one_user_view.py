from typing import Dict
import logging

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from mongoengine.errors import DoesNotExist

from .users_blp import users_blp

from ...schemas.users_schemas import (
    InputUpdateUserSchema,
    UserResponseSchema
)

from ...models.user import User
from ....helpers.errors_msg_handler import BadRequest, ReasonError


logger = logging.getLogger('console')


@users_blp.route('/<int:user_id>')
class OneUserView(MethodView):

    @users_blp.doc(operationId='UpdateUser')
    @users_blp.arguments(InputUpdateUserSchema)
    @users_blp.response(200, schema=UserResponseSchema, description="Update one user")
    @jwt_required()
    def put(self, input_dict: Dict, user_id: int):
        try:
            user = User.get_by_id(id=user_id)
        except DoesNotExist:
            raise BadRequest(f"User #{user_id} not found !")
        
        user.update(input_dict)
        user.save()

        return {
            "action": "updated",
            "user": user
        }


    @users_blp.doc(operationId='DeleteUser')
    @users_blp.response(200, schema=UserResponseSchema, description="Delete one user")
    @jwt_required()
    def delete(self, user_id: int):
        try:
            user = User.get_by_id(id=user_id)
        except DoesNotExist:
            raise BadRequest(f"User #{user_id} not found !")
        
        user.delete()

        return {
            "action": "deleted",
            "user": user
        }
