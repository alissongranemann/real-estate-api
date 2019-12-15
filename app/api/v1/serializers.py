from marshmallow import Schema, fields, validates, ValidationError
import re


class FederalUnitySchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    short_name = fields.String(required=True)


class CitySchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    federal_unity = fields.Nested(FederalUnitySchema(), required=True, dump_only=True)


class NeighbourhoodSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    city = fields.Nested(CitySchema(), required=True, dump_only=True)


class PostalCodeSchema(Schema):
    id = fields.Integer()
    code = fields.String(required=True)
    city = fields.Nested(CitySchema(), required=True, dump_only=True)

    @validates("code")
    def validate_postal_code(self, value):
        regex = re.compile(r"[0-9]{5}-[0-9]{3}")
        if not regex.match(value):
            raise ValidationError("postal_code must follow the #####-### pattern.")


class StreetSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    postal_code = fields.Nested(PostalCodeSchema(), required=True, dump_only=True)
    neighbourhood = fields.Nested(NeighbourhoodSchema(), required=True, dump_only=True)


class LocationSchema(Schema):
    id = fields.Integer()
    street = fields.Nested(StreetSchema(), required=True, dump_only=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    places_id = fields.String(required=True)
    postal_code = fields.String(required=True, load_only=True)


class PropertySchema(Schema):
    id = fields.Integer(dump_only=True)
    area = fields.Integer(required=True)
    price = fields.Float(required=True)
    location = fields.Nested(LocationSchema(), required=True, dump_only=True)
    postal_code = fields.String(required=True, load_only=True)
    url = fields.String(required=True, load_only=True)

    @validates("postal_code")
    def validate_postal_code(self, value):
        regex = re.compile(r"[0-9]{5}-[0-9]{3}")
        if not regex.match(value):
            raise ValidationError("postal_code must follow the #####-### pattern.")


class AddressComponentLongName(fields.Field):
    def _deserialize(self, obj, attr, data, **kwargs):
        if obj is None:
            return None
        return obj.get("long_name")


class AddressComponentShortName(fields.Field):
    def _deserialize(self, obj, attr, data, **kwargs):
        if obj is None:
            return None
        return obj.get("short_name")


class AddressComponentShortLongName(fields.Field):
    def _deserialize(self, obj, attr, data, **kwargs):
        if obj is None:
            return None
        return (obj.get("short_name"), obj.get("long_name"))


class PlaceReaderSchema(Schema):
    places_id = fields.String(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    street = AddressComponentLongName()
    neighbourhood = AddressComponentLongName()
    city = AddressComponentLongName(required=True)
    federal_unity = AddressComponentShortLongName(required=True)
    postal_code = AddressComponentShortName(required=True)
