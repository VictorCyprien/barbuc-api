from flask.views import MethodView

from ...models.user import User

class AbstractUsersView(MethodView):

    authenticated_user: User = None

    def set_authenticated_user(self, authenticated_user: User):
        self.authenticated_user = authenticated_user
