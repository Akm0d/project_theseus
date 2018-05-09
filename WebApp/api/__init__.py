from flask import Blueprint
from flask_restful import Api
from WebApp.api.resources import *

resource = Blueprint('api', __name__, url_prefix='/api')
api = Api(resource)

# for c in dir(resources):
#     t = getattr(resources, c)
#     if isinstance(t, type) and issubclass(t, Resource):
#         base = t.url if hasattr(t, "url") else c.lower()
#         api.add_resource(t, "/{base}/".format(base=base), "/{base}/<arg>".format(base=base))

api.add_resource(Keypad, '/keycode/', '/keycode/<code>')
api.add_resource(RGB, '/rgb_status/', '/rgb_status/<color>')
api.add_resource(Solenoid, '/solenoid/<action>')
api.add_resource(Timer, '/timer/<action>')
api.add_resource(Tripwire, '/tripwire/<name>/<action>')
api.add_resource(TripwireAll, '/tripwire/all/<action>')
api.add_resource(Randomize, '/tripwire/randomize')
api.add_resource(Ultrasonic, '/ultrasonic/<action>')
api.add_resource(Team, '/team/', '/team/<name>')
api.add_resource(Attempts, '/attempts/')
api.add_resource(Successes, '/successes/')
api.add_resource(HighScores, '/high-scores/')
api.add_resource(TimerText, '/timer-text/')
