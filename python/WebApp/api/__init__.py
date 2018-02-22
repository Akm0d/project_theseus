import logging

from flask import Blueprint
from flask_restful import Api

from .. import app
from .resources import Keypad, RGB, Randomize, Solenoid, Test, Timer, Tripwire, TripwireAll, Ultrasonic

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
app.register_blueprint(blueprint)

api.add_resource(Keypad, '/keycode', '/keycode/<code>')
api.add_resource(RGB, '/rgb_select/<color>')
api.add_resource(Solenoid, '/solenoid/<action>')
api.add_resource(Timer, '/timer/<action>')
api.add_resource(Tripwire, '/tripwire/<name>/<action>')
api.add_resource(TripwireAll, '/tripwire/all/<action>')
api.add_resource(Randomize, '/tripwire/randomize')
api.add_resource(Ultrasonic, '/ultrasonic/<action>')
api.add_resource(Test, '/test/<var>')
