from typing import List
import logging

from flask.views import MethodView

logger = logging.getLogger('console')


class AbstractBarbecuesView(MethodView):
    def can_read_the_barbecue(self, user_scopes: List[str]) -> bool:
        return "user:admin" in user_scopes
