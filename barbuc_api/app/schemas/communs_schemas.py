from marshmallow import Schema, fields, pre_load, pre_dump


class PagingError(Schema):
    code = fields.Integer(metadata={"description": "Error status code"})
    message = fields.String(metadata={"description": "Error message"})
    status = fields.String(metadata={"description": "Error status"})

    class Meta:
        description = "Informations about the error"
        ordered = True
