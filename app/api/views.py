from flask_restful import Resource, reqparse, request, abort

from app.models import Property, Location, State
from app.api.serializers import PropertySchema, PlaceReaderSchema
from app import db, logger
from marshmallow import ValidationError
from app.gmaps import get_place_by_postal_code
from geoalchemy2 import WKTElement

parser = reqparse.RequestParser()


class PropertyList(Resource):
    def get(self):
        parser.add_argument("page", type=float, help="Page index.", required=False)
        parser.add_argument(
            "page_size", type=int, help="Page max size.", required=False
        )
        args = parser.parse_args()

        page = args.get("page", 1)
        page_size = args.get("page_size", 10)
        property_list = Property.query.paginate(page, page_size, False)
        schema = PropertySchema(many=True)
        result = schema.dump(property_list.items)

        return dict(
            data=result,
            total=property_list.total,
            current_page=property_list.page,
            per_page=property_list.per_page,
            num_pages=property_list.pages,
        )

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            abort(400)
        try:
            result = PropertySchema().load(json_data)
        except ValidationError as err:
            abort(400, errors=err.messages)

        postal_code = result["postal_code"]
        location = self.get_location(postal_code)
        property = Property(
            price=result.get("price"), area=result.get("area"), location=location
        )
        db.session.add(property)
        db.session.commit()

        return "", 201

    def get_location(self, postal_code):
        location = Location.query.filter_by(postal_code=postal_code).one_or_none()
        if location is None:
            raw_place = get_place_by_postal_code(postal_code)
            if raw_place is None:
                return (
                    {"errors": ["No place was found with the provided postal code."]},
                    400,
                )
            try:
                place = PlaceReaderSchema().load(raw_place)
            except ValidationError as err:
                logger.info(f"Google Places API returned an invalid value: {raw_place}")
                logger.info(f"Validation error: {err}")
                return ({"errors": ["Internal error."]}, 400)

            place = PlaceReaderSchema().load(raw_place)
            state = self.get_state(place["state"])
            longitude = place["longitude"]
            latitude = place["latitude"]
            geom = WKTElement(f"POINT({longitude} {latitude})")
            location = Location(
                state=state,
                postal_code=postal_code,
                street=place.get("street"),
                neighbourhood=place.get("neighbourhood"),
                city=place.get("city"),
                latitude=longitude,
                longitude=latitude,
                places_id=place["places_id"],
                geom=geom,
            )

        return location

    def get_state(self, state_data):
        state_initials = state_data[0]
        state = State.query.filter_by(initials=state_initials).one_or_none()
        if state is None:
            state = State(initials=state_initials, description=state_data[1])

        return state


class PropertyDetail(Resource):
    def delete(self, id):
        property = Property.query.get_or_404(id)
        db.session.delete(property)
        db.session.commit()
        return "", 204

    def get(self, id):
        schema = PropertySchema()
        property = Property.query.get_or_404(id)
        result = schema.dump(property)
        return result
