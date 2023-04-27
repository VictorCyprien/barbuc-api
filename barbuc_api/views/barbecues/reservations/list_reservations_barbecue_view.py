import logging

from flask_jwt_extended import jwt_required, get_jwt_identity

from ..barbecues_blp import barbecues_blp
from ..abstract_barbecue_view import AbstractBarbecuesView

from ....schemas.communs_schemas import PagingError
from ....schemas.reservation_barbecue_schemas import (
    GetBarbecuesReservationsListSchema
)

from ....models.user import User


logger = logging.getLogger('console')


@barbecues_blp.route('/availables')
class ListBarbecuesReservationsView(AbstractBarbecuesView):

    @barbecues_blp.doc(operationId='ListReservationsBarbecues')
    @barbecues_blp.response(401, schema=PagingError, description="Unauthorized")
    @barbecues_blp.response(200, schema=GetBarbecuesReservationsListSchema, description="List all the current reservations barbecue")
    @jwt_required()
    def get(self):
        """List the current reservations of barbecues"""
        auth_user = User.get_by_id(get_jwt_identity())
        result = self.can_see_all_reserved_barbecue(auth_user.scopes, auth_user.user_id)

        return {
            "reservations": result
        }

