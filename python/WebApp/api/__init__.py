from flask import Blueprint, current_app as app
from flask_restful import Api, Resource

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint)

class Test(Resource):
    # GET request will call this function
    def get(self):
        return {"Hello":"World"}

api.add_resource(Test, '/test')
