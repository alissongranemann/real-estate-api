from marshmallow import Schema, fields, validates, ValidationError
import re


class AddressSchema(Schema):

    id = fields.Integer()
    city = fields.String(required=True)
    neighbourhood = fields.String()
    cep = fields.String(required=True)

    @validates("cep")
    def validate_cep(self, value):
        regex = re.compile(r"[0-9]{5}-[0-9]{3}")
        if not regex.match(value):
            raise ValidationError("Cep must follow the #####-### pattern.")


class PropertySchema(Schema):
    id = fields.Integer()
    area = fields.Integer(required=True)
    price = fields.Float(required=True)
    address = fields.Nested(AddressSchema(), required=True)
