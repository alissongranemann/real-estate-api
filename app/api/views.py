from flask_restful import Resource, reqparse, request, abort

from app.models import Property, Address
from app.api.serializers import PropertySchema
from app import db
from marshmallow import ValidationError


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
            return {"errors": err.messages}, 400

        address = Address(**result["address"])
        property = Property(
            price=result.get("price"), area=result.get("area"), address=address
        )
        db.session.add(property)
        db.session.commit()

        return "", 201


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
