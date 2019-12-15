from flask_restful import Resource, reqparse, request, abort
import logging

from app.api.v1.serializers import PropertySchema
from app.services import (
    property_exists,
    get_property,
    get_property_list,
    save_property,
    delete_property,
    get_location_by_postal_code,
    create_location,
)
from marshmallow import ValidationError

parser = reqparse.RequestParser()

LOG = logging.getLogger(__name__)


class PropertyList(Resource):
    def get(self):
        parser.add_argument("page", type=float, help="Page index.", required=False)
        parser.add_argument(
            "page_size", type=int, help="Page max size.", required=False
        )
        args = parser.parse_args()

        page = args.get("page", 1)
        page_size = args.get("page_size", 10)
        property_list = get_property_list(page, page_size)
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
            LOG.error(err)
            abort(400, errors=err.messages)

        postal_code = result["postal_code"]
        price = result.get("price")
        area = result.get("area")
        url = result.get("url")
        if property_exists(postal_code, price, area):
            return "", 303
        try:
            location = get_location_by_postal_code(postal_code)
            if location is None:
                location = create_location(postal_code)

            property = save_property(location, price, area, url)
        except Exception as err:
            LOG.error(f"Error while creating a property: {err}")
            abort(400, errors=[err])

        schema = PropertySchema()
        return schema.dump(property), 201


class PropertyDetail(Resource):
    def delete(self, id):
        delete_property(id)
        return "", 204

    def get(self, id):
        schema = PropertySchema()
        result = schema.dump(get_property(id))
        return result
