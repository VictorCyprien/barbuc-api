from typing import Dict
import logging

from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import ValidationError

from .barbucues_blp import barbucues_blp
from .abstract_barbucue_view import AbstractBarbucuesView

from ...schemas.communs_schemas import PagingError
from ...schemas.barbucue_schemas import (
    InputUpdateBarbucueSchema,
    BarbucueResponseSchema
)

from ...models.user import User
from ...models.barbucue import Barbucue
from ...helpers.errors_msg_handler import BadRequest, ReasonError, NotFound


logger = logging.getLogger('console')


@barbucues_blp.route('/<int:barbucue_id>')
class OneUserView(AbstractBarbucuesView):

    @barbucues_blp.doc(operationId='UpdateBarbucue')
    @barbucues_blp.arguments(InputUpdateBarbucueSchema)
    @barbucues_blp.response(400, schema=PagingError, description="BadRequest")
    @barbucues_blp.response(404, schema=PagingError, description="NotFound")
    @barbucues_blp.response(200, schema=BarbucueResponseSchema, description="Update one barbucue")
    @jwt_required()
    def put(self, input_dict: Dict, barbucue_id: int):
        """Update an existing barbucue"""
        auth_user = User.get_by_id(get_jwt_identity())
        
        if not self.can_read_the_barbucue(auth_user.scopes):
            raise NotFound(f"Barbucue #{barbucue_id} not found !")

        barbucue = Barbucue.get_by_id(id=barbucue_id)
        barbucue.update(input_dict)
        
        try:
            barbucue.save()
        except ValidationError:
            raise BadRequest(ReasonError.UPDATE_BARBUCUE_ERROR.value)

        return {
            "action": "updated",
            "barbucue": barbucue
        }


    @barbucues_blp.doc(operationId='DeleteBarbucue')
    @barbucues_blp.response(400, schema=PagingError, description="BadRequest")
    @barbucues_blp.response(404, schema=PagingError, description="NotFound")
    @barbucues_blp.response(200, schema=BarbucueResponseSchema, description="Delete one barbucue")
    @jwt_required()
    def delete(self, barbucue_id: int):
        """Delete an existing barbucue"""
        auth_user = User.get_by_id(get_jwt_identity())
        
        if not self.can_read_the_barbucue(auth_user.scopes):
            raise NotFound(f"Barbucue #{barbucue_id} not found !")

        barbucue = Barbucue.get_by_id(id=barbucue_id)
        barbucue.delete()

        return {
            "action": "deleted",
            "barbucue": barbucue
        }
