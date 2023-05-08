from marshmallow import Schema, fields, post_dump
from marshmallow.validate import Range

from ..schemas.users_schemas import UserSchema

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
    user = fields.Nested(
        UserSchema,
        only=('user_id', 'name'),
        metadata={
            "exclude_if_null": True,
            "description": "User who reserved the barbecue",
        }
    )

    @post_dump
    def exclude_if_null(self, in_data, **kwargs):
        for key, value in self.fields.items():
            if value.metadata.get('exclude_if_null') and key in in_data and in_data[key] is None:
                del in_data[key]
            if value.metadata.get('exclude_if_empty') and hasattr(in_data.get(key) , '__len__') and len(in_data.get(key)) == 0:
                del in_data[key]
        return in_data
    
    class Meta:
        ordered = True
        description = "Barbecue informations."



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
