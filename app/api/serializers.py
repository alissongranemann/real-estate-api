from marshmallow import Schema, fields


class AddressSchema(Schema):
    class Meta:
        fields = ("id", "city", "neighbourhood", "cep")


class PropertySchema(Schema):
    id = fields.Integer()
    area = fields.Integer(required=True)
    price = fields.Float(required=True)
    address = fields.Nested(AddressSchema())
