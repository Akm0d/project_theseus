from flask import Blueprint, current_app as app, request
from flask_restful import Api, Resource

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)


@api.resource('/test/<var>')
class Test(Resource):
    def get(self, var: str):
        return {"status": var}
