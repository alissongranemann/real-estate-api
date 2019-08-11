from flask_restful import Resource, reqparse
from flask import jsonify

from ..models import Property
from .. import db


class PropertyList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("page", type=float, help="Page index.", required=False)
        parser.add_argument(
            "page_limit", type=int, help="Page max size.", required=False
        )
        args = parser.parse_args()

        page = args.get("page", 1)
        page_limit = args.get("page_limit", 10)
        property_list = Property.query.paginate(page, page_limit, False)

        return dict(
            data=[property.to_json() for property in property_list.items],
            total=property_list.total,
            current_page=property_list.page,
            per_page=property_list.per_page,
        )

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("price", type=float, help="Property's price value.")
        parser.add_argument("area", type=int, help="Property's area value.")
        args = parser.parse_args()

        property = Property(**args)
        db.session.add(property)
        db.session.commit()
        return {"property": property.to_json()}, 201
