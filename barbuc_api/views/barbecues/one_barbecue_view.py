from typing import Dict
import logging

from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import ValidationError

from .barbecues_blp import barbecues_blp
from .abstract_barbecue_view import AbstractBarbecuesView

from ...schemas.communs_schemas import PagingError
from ...schemas.barbecue_schemas import (
    InputUpdateBarbecueSchema,
    BarbecueResponseSchema
)

from ...models.user import User
from ...models.barbecue import Barbecue
from ...helpers.errors_msg_handler import BadRequest, ReasonError, NotFound


logger = logging.getLogger('console')


@barbecues_blp.route('/<int:barbecue_id>')
class OneBarbecueView(AbstractBarbecuesView):

    @barbecues_blp.doc(operationId='UpdateBarbecue')
    @barbecues_blp.arguments(InputUpdateBarbecueSchema)
    @barbecues_blp.response(400, schema=PagingError, description="BadRequest")
    @barbecues_blp.response(404, schema=PagingError, description="NotFound")
    @barbecues_blp.response(200, schema=BarbecueResponseSchema, description="Update one barbecue")
    @jwt_required()
    def put(self, input_dict: Dict, barbecue_id: int):
        """Update an existing barbecue"""
        auth_user = User.get_by_id(get_jwt_identity())
        
        if not self.can_read_the_barbecue(auth_user.scopes):
            raise NotFound(f"Barbecue #{barbecue_id} not found !")

        barbecue = self.get_barbecue(barbecue_id)
        barbecue.update(input_dict)
        
        try:
            barbecue.save()
        except ValidationError:
            raise BadRequest(ReasonError.UPDATE_BARBECUE_ERROR.value)

        return {
            "action": "updated",
            "barbecue": barbecue
        }


    @barbecues_blp.doc(operationId='DeleteBarbecue')
    @barbecues_blp.response(400, schema=PagingError, description="BadRequest")
    @barbecues_blp.response(404, schema=PagingError, description="NotFound")
    @barbecues_blp.response(200, schema=BarbecueResponseSchema, description="Delete one barbecue")
    @jwt_required()
    def delete(self, barbecue_id: int):
        """Delete an existing barbecue"""
        auth_user = User.get_by_id(get_jwt_identity())
        
        if not self.can_read_the_barbecue(auth_user.scopes):
            raise NotFound(f"Barbecue #{barbecue_id} not found !")

        barbecue = Barbecue.get_by_id(id=barbecue_id)
        barbecue.delete()

        return {
            "action": "deleted",
            "barbecue": barbecue
        }
