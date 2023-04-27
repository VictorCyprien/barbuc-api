from typing import Dict
import logging

from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import ValidationError, DoesNotExist

from ..barbecues_blp import barbecues_blp
from ..abstract_barbecue_view import AbstractBarbecuesView

from ....schemas.communs_schemas import PagingError
from ....schemas.reservation_barbecue_schemas import (
    BarbecueAvailableReponse
)

from ....models.user import User
from ....models.barbecue import Barbecue
from ....helpers.errors_msg_handler import BadRequest, ReasonError, NotFound


logger = logging.getLogger('console')


@barbecues_blp.route('/<int:barbecue_id>/available')
class OneBarbecueAvailableView(AbstractBarbecuesView):

    @barbecues_blp.doc(operationId='CheckBarbecueAvailable')
    @barbecues_blp.response(404, schema=PagingError, description="NotFound")
    @barbecues_blp.response(200, schema=BarbecueAvailableReponse, description="Check if one barbecue is avaiable")
    @jwt_required()
    def get(self, barbecue_id: int):
        """Check if the barbecue is available"""
        barbecue = self.get_barbecue(barbecue_id)
        available = barbecue.user is None

        return {
            "is_available": available
        }
