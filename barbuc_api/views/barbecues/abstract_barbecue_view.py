from typing import List
import logging

from mongoengine.errors import DoesNotExist

from flask.views import MethodView

from ...models.barbecue import Barbecue
from ...helpers.errors_msg_handler import NotFound

logger = logging.getLogger('console')


class AbstractBarbecuesView(MethodView):
    def can_read_the_barbecue(self, user_scopes: List[str]) -> bool:
        return "user:admin" in user_scopes

    def can_see_all_reserved_barbecue(self, user_scopes: List[str], user_id: int) -> bool:
        query = Barbecue.objects(user__ne=None)
        if "user:admin" not in user_scopes:
            query = query.filter(user=user_id)
        return query

    def get_barbecue(self, barbecue_id: int):
        try:
            return Barbecue.get_by_id(barbecue_id)
        except DoesNotExist:
            raise NotFound(f"Barbecue #{barbecue_id} not found !")
