from typing import List, Set, Optional
import logging

from mongoengine.errors import DoesNotExist, ValidationError
from mongoengine.queryset.visitor import Q

from flask.views import MethodView

from ...models.user import User

logger = logging.getLogger('console')


class AbstractUsersView(MethodView):
    def can_read_the_user(self, auth_user_id: int, user_scopes: List[str], user_id: int) -> bool:
        return user_id == auth_user_id or "user:admin" in user_scopes
