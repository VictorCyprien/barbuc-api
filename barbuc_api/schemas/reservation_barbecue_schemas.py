from marshmallow import Schema, fields
from marshmallow.validate import Range

from ..models.barbecue import BARBUC_ID_MAX_VAL

from ..schemas.barbecue_schemas import BarbecueSchema
from ..schemas.users_schemas import UserSchema


class BarbecueAvailableReponse(Schema):
    is_available = fields.Boolean(
        metadata={"description": "Is barbecue available ?"}
    )

    class Meta:
        ordered = True


class BarbecueReservationReponse(Schema):
    action = fields.String(metadata={"description": "Status of the reservation"})
    barbecue = fields.Nested(
        BarbecueSchema,
        metadata={"description": "Reserved barbecue"}
    )

    class Meta:
        ordered = True


class BarbecueCancelReservationReponse(Schema):
    action = fields.String(metadata={"description": "Status of the reservation"})
    barbecue = fields.Nested(
        BarbecueSchema,
        metadata={"description": "Canceled reservation barbecue"}
    )
    user = fields.Nested(
        UserSchema,
        metadata={"description": "User who canceled the reservation"}
    )

    class Meta:
        ordered = True


class GetBarbecuesReservationsListSchema(Schema):
    reservations = fields.Nested(BarbecueSchema, many=True)

    class Meta:
        ordered = True
