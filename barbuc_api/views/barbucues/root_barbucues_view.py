import logging

from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import NotUniqueError, ValidationError

from .barbucues_blp import barbucues_blp
from .abstract_barbucue_view import AbstractBarbucuesView

from ...schemas.communs_schemas import PagingError
from ...schemas.barbucue_schemas import (
    GetBarbucuesListSchema,
    InputCreateBarbucueSchema,
    BarbucueResponseSchema
)

from ...models.barbucue import Barbucue
from ...models.user import User
from ...helpers.errors_msg_handler import BadRequest, ReasonError, Unauthorized


logger = logging.getLogger('console')


@barbucues_blp.route('/')
class RootBarbucuesView(AbstractBarbucuesView):

    @barbucues_blp.doc(operationId='ListBarbucues')
    @barbucues_blp.response(401, schema=PagingError, description="Unautorized")
    @barbucues_blp.response(200, schema=GetBarbucuesListSchema, description="List of barbucues found in the database")
    @jwt_required()
    def get(self):
        """Retrieve list of barbucues"""
        auth_user = User.get_by_id(get_jwt_identity())
        if not self.can_read_the_barbucue(auth_user.scopes):
            raise Unauthorized(ReasonError.BAD_SCOPES.value)

        barbucues = Barbucue.objects()

        return {
            'barbucues': barbucues,
        }


    @barbucues_blp.doc(operationId='CreateBarbucue')
    @barbucues_blp.arguments(InputCreateBarbucueSchema)
    @barbucues_blp.response(400, schema=PagingError, description="BadRequest")
    @barbucues_blp.response(401, schema=PagingError, description="Unautorized")
    @barbucues_blp.response(201, schema=BarbucueResponseSchema, description="Infos of new barbucue")
    @jwt_required()
    def post(self, input_data: dict):
        """Create a new barbucue"""
        auth_user = User.get_by_id(get_jwt_identity())
        if not self.can_read_the_barbucue(auth_user.scopes):
            raise Unauthorized(ReasonError.BAD_SCOPES.value)
        
        barbucue = Barbucue.create(input_data=input_data)
        barbucue.save()

        return {
            'action': 'created',
            'barbucue': barbucue
        }
