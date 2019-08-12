from flask import Blueprint
from flask_restful import Api

from .views import PropertyList, PropertyDetail

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)


api.add_resource(PropertyList, "/properties")
api.add_resource(PropertyDetail, "/properties/<int:id>")
