import logging

from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import NotUniqueError, ValidationError

from .barbecues_blp import barbecues_blp
from .abstract_barbecue_view import AbstractBarbecuesView

from ...schemas.communs_schemas import PagingError
from ...schemas.barbecue_schemas import (
    GetBarbecuesListSchema,
    InputCreateBarbecueSchema,
    BarbecueResponseSchema
)

from ...models.barbecue import Barbecue
from ...models.user import User
from ...helpers.errors_msg_handler import BadRequest, ReasonError, Unauthorized


logger = logging.getLogger('console')


@barbecues_blp.route('/')
class RootBarbecuesView(AbstractBarbecuesView):

    @barbecues_blp.doc(operationId='ListBarbecues')
    @barbecues_blp.response(401, schema=PagingError, description="Unautorized")
    @barbecues_blp.response(200, schema=GetBarbecuesListSchema, description="List of barbecues found in the database")
    @jwt_required()
    def get(self):
        """Retrieve list of barbecues"""
        auth_user = User.get_by_id(get_jwt_identity())
        if not self.can_read_the_barbecue(auth_user.scopes):
            raise Unauthorized(ReasonError.BAD_SCOPES.value)

        barbecues = Barbecue.objects()

        return {
            'barbecues': barbecues,
        }


    @barbecues_blp.doc(operationId='CreateBarbecue')
    @barbecues_blp.arguments(InputCreateBarbecueSchema)
    @barbecues_blp.response(400, schema=PagingError, description="BadRequest")
    @barbecues_blp.response(401, schema=PagingError, description="Unautorized")
    @barbecues_blp.response(201, schema=BarbecueResponseSchema, description="Infos of new barbecue")
    @jwt_required()
    def post(self, input_data: dict):
        """Create a new barbecue"""
        auth_user = User.get_by_id(get_jwt_identity())
        if not self.can_read_the_barbecue(auth_user.scopes):
            raise Unauthorized(ReasonError.BAD_SCOPES.value)
        
        barbecue = Barbecue.create(input_data=input_data)
        
        try:
            barbecue.save()
        except ValidationError:
            raise BadRequest(ReasonError.CREATE_BARBECUE_ERROR.value)

        return {
            'action': 'created',
            'barbecue': barbecue
        }
