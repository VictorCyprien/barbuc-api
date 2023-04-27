from typing import List
import logging

from flask.views import MethodView

from ...models.barbecue import Barbecue

logger = logging.getLogger('console')


class AbstractBarbecuesView(MethodView):
    def can_read_the_barbecue(self, user_scopes: List[str]) -> bool:
        return "user:admin" in user_scopes

    def can_see_all_reserved_barbecue(self, user_scopes: List[str], user_id: int) -> bool:
        if "user:admin" in user_scopes:
            return Barbecue.objects(user__ne=None)
        else:
            return Barbecue.objects(user__ne=None, user=user_id)
