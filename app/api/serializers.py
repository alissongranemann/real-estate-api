from marshmallow import Schema, fields


class AddressSchema(Schema):
    class Meta:
        fields = ("id", "city", "neighbourhood", "cep")


class PropertySchema(Schema):
    address = fields.Nested(AddressSchema())

    class Meta:
        fields = ("id", "area", "price", "address")
