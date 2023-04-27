import logging

from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import ValidationError

from ..barbecues_blp import barbecues_blp
from ..abstract_barbecue_view import AbstractBarbecuesView

from ....schemas.communs_schemas import PagingError
from ....schemas.reservation_barbecue_schemas import (
    BarbecueReservationReponse
)

from ....models.user import User
from ....helpers.errors_msg_handler import BadRequest, ReasonError, Unauthorized


logger = logging.getLogger('console')


@barbecues_blp.route('/<int:barbecue_id>/reserve')
class OneBarbecueReservationView(AbstractBarbecuesView):

    @barbecues_blp.doc(operationId='ReserveBarbecue')
    @barbecues_blp.response(404, schema=PagingError, description="NotFound")
    @barbecues_blp.response(401, schema=PagingError, description="The barbecue is already reserved !")
    @barbecues_blp.response(201, schema=BarbecueReservationReponse, description="Reserve the current barbecue")
    @jwt_required()
    def post(self, barbecue_id: int):
        """Reserve the current barbecue"""
        barbecue = self.get_barbecue(barbecue_id)
        if barbecue.user is not None:
            raise Unauthorized(ReasonError.BARBECUE_ALREADY_RESERVED.value)
        
        auth_user = User.get_by_id(get_jwt_identity())
        barbecue.user = auth_user
        
        try:
            barbecue.save()
        except ValidationError:
            raise BadRequest(ReasonError.UPDATE_BARBECUE_ERROR.value)

        return {
            "action": "reserved",
            "barbecue": barbecue,
            "user": barbecue.user
        }
