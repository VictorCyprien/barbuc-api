from typing import Dict
import logging

from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import ValidationError, DoesNotExist

from ..barbecues_blp import barbecues_blp
from ..abstract_barbecue_view import AbstractBarbecuesView

from ....schemas.communs_schemas import PagingError
from ....schemas.reservation_barbecue_schemas import (
    BarbecueCancelReservationReponse
)

from ....models.user import User
from ....models.barbecue import Barbecue
from ....helpers.errors_msg_handler import BadRequest, ReasonError, NotFound, Unauthorized


logger = logging.getLogger('console')


@barbecues_blp.route('/<int:barbecue_id>/cancel')
class OneBarbecueCancelReservationView(AbstractBarbecuesView):

    @barbecues_blp.doc(operationId='CancelReservationBarbecue')
    @barbecues_blp.response(404, schema=PagingError, description="NotFound")
    @barbecues_blp.response(401, schema=PagingError, description="The barbecue is not reserved !")
    @barbecues_blp.response(201, schema=BarbecueCancelReservationReponse, description="Cancel the reservation of the current barbecue")
    @jwt_required()
    def post(self, barbecue_id: int):
        """Cancel the reservation of the current barbecue"""
        barbecue = self.get_barbecue(barbecue_id)
        
        if barbecue.user is None:
            raise Unauthorized(ReasonError.BARBECUE_NOT_RESERVED.value)
        
        auth_user = User.get_by_id(get_jwt_identity())

        if barbecue.user.user_id != auth_user.user_id:
            raise Unauthorized(ReasonError.BARBECUE_CANCEL_RESERVATION_REFUSED.value)

        barbecue.user = None
        
        try:
            barbecue.save()
        except ValidationError:
            raise BadRequest(ReasonError.UPDATE_BARBECUE_ERROR.value)

        return {
            "action": "canceled",
            "barbecue": barbecue,
            "user": auth_user
        }
