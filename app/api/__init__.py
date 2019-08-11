from flask import Blueprint
from flask_restful import Api

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

from .views import PropertyList
api.add_resource(PropertyList, "/properties")
