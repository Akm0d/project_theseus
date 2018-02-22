import logging

from flask import Blueprint
from flask_restful import Api

from .. import app
from .resources import Test

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
app.register_blueprint(blueprint)

api.add_resource(Test, '/test/<var>')
