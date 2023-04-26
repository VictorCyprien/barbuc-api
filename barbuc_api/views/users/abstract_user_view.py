from typing import List
import logging

from flask.views import MethodView

logger = logging.getLogger('console')


class AbstractUsersView(MethodView):
    def can_read_the_user(self, auth_user_id: int, user_scopes: List[str], user_id: int) -> bool:
        return user_id == auth_user_id or "user:admin" in user_scopes
