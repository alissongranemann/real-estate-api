from marshmallow import Schema, fields, validates, ValidationError
import re


class StateSchema(Schema):
    id = fields.Integer()
    description = fields.String(required=True)
    initials = fields.String(required=True)


class LocationSchema(Schema):
    id = fields.Integer()
    postal_code = fields.String(required=True)
    route = fields.String(required=True, load_only=True)
    sublocality = fields.String(required=True, load_only=True)
    city = fields.String(required=True, load_only=True)
    latitude = fields.Float(required=True, load_only=True)
    longitude = fields.Float(required=True, load_only=True)
    # geom = db.Column(Geometry("POINT"), nullable=False)
    state = fields.Nested(StateSchema(), required=True, load_only=True)

    @validates("cep")
    def validate_cep(self, value):
        regex = re.compile(r"[0-9]{5}-[0-9]{3}")
        if not regex.match(value):
            raise ValidationError("Cep must follow the #####-### pattern.")


class PropertySchema(Schema):
    id = fields.Integer()
    area = fields.Integer(required=True)
    price = fields.Float(required=True)
    location = fields.Nested(LocationSchema(), required=True)
