from typing import List
import logging

from flask.views import MethodView

logger = logging.getLogger('console')


class AbstractBarbucuesView(MethodView):
    def can_read_the_barbucue(self, user_scopes: List[str]) -> bool:
        return "user:admin" in user_scopes
