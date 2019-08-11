from flask import Blueprint
from flask_restful import Api

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

from .views import HelloWorld
api.add_resource(HelloWorld, "/")
