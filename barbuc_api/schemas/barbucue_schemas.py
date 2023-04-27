from marshmallow import Schema, fields
from marshmallow.validate import Range

from ..models.barbucue import BARBUC_ID_MAX_VAL

class BarbucueSchema(Schema):
    barbuc_id = fields.Integer(
        attribute='barbuc_id',
        validate=Range(min=0, min_inclusive=False, max=BARBUC_ID_MAX_VAL, max_inclusive=False),
        metadata={"description": "Unique barbucue identifier"}
    )
    name = fields.String(metadata={"description": "Name of the barbucue"}, required=True)
    place = fields.String(metadata={"description": "Place of the barbucue"}, required=True)
    _date = fields.String(
        format="date-time",
        data="date",
        metadata={"description": "Date of the barbucue"},
        required=True
    )


class BarbucueResponseSchema(Schema):
    action = fields.String()
    barbucue = fields.Nested(BarbucueSchema)

    class Meta:
        ordered = True
        description = "Create/Update/Delete a barbucue."


class GetBarbucuesListSchema(Schema):
    barbucues = fields.Nested(BarbucueSchema, many=True)

    class Meta:
        description = "List of barbucues."
        ordered = True


class InputCreateBarbucueSchema(Schema):
    name = fields.String(metadata={"description": "Name of the barbucue"}, required=True)
    place = fields.String(metadata={"description": "Place of the barbucue"}, required=True)
    date = fields.String(
        format="date-time",
        metadata={"description": "Date of the barbucue"}, 
        required=True
    )

    class Meta:
        description = "Input informations need to create barbucue."
        ordered = True



class InputUpdateBarbucueSchema(Schema):
    name = fields.String(metadata={"description": "New name of the barbucue"}, required=False)
    place = fields.String(metadata={"description": "New place of the barbucue"}, required=False)
    date = fields.String(
        format="date-time",
        metadata={"description": "New date of the barbucue"}, 
        required=False
    )

    class Meta:
        description = "Input informations need to update a barbucue."
        ordered = True
