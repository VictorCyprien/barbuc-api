from marshmallow import Schema, fields
from marshmallow.validate import Range

from ..models.barbecue import BARBUC_ID_MAX_VAL

class BarbecueSchema(Schema):
    barbecue_id = fields.Integer(
        attribute='barbecue_id',
        validate=Range(min=0, min_inclusive=False, max=BARBUC_ID_MAX_VAL, max_inclusive=False),
        metadata={"description": "Unique barbecue identifier"}
    )
    name = fields.String(metadata={"description": "Name of the barbecue"}, required=True)
    place = fields.String(metadata={"description": "Place of the barbecue"}, required=True)
    _date = fields.String(
        format="date-time",
        data="date",
        metadata={"description": "Date of the barbecue"},
        required=True
    )


class BarbecueResponseSchema(Schema):
    action = fields.String()
    barbecue = fields.Nested(BarbecueSchema)

    class Meta:
        ordered = True
        description = "Create/Update/Delete a barbecue."


class GetBarbecuesListSchema(Schema):
    barbecues = fields.Nested(BarbecueSchema, many=True)

    class Meta:
        description = "List of barbecues."
        ordered = True


class InputCreateBarbecueSchema(Schema):
    name = fields.String(metadata={"description": "Name of the barbecue"}, required=True)
    place = fields.String(metadata={"description": "Place of the barbecue"}, required=True)
    date = fields.String(
        format="date-time",
        metadata={"description": "Date of the barbecue"}, 
        required=True
    )

    class Meta:
        description = "Input informations need to create barbecue."
        ordered = True



class InputUpdateBarbecueSchema(Schema):
    name = fields.String(metadata={"description": "New name of the barbecue"}, required=False)
    place = fields.String(metadata={"description": "New place of the barbecue"}, required=False)
    date = fields.String(
        format="date-time",
        metadata={"description": "New date of the barbecue"}, 
        required=False
    )

    class Meta:
        description = "Input informations need to update a barbecue."
        ordered = True
