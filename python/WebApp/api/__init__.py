from flask import Blueprint
from flask_restful import Api
from WebApp.api.resources import Keypad, RGB, Solenoid, Timer, Tripwire, TripwireAll, Randomize, Ultrasonic, Entry, PlayGame, Attempts, Successes, HighScores, TimerText

resource = Blueprint('api', __name__, url_prefix='/api')
api = Api(resource)

api.add_resource(Keypad, '/keycode/', '/keycode/<code>')
api.add_resource(RGB, '/rgb_select/<color>')
api.add_resource(Solenoid, '/solenoid/<action>')
api.add_resource(Timer, '/timer/<action>')
api.add_resource(Tripwire, '/tripwire/<name>/<action>')
api.add_resource(TripwireAll, '/tripwire/all/<action>')
api.add_resource(Randomize, '/tripwire/randomize')
api.add_resource(Ultrasonic, '/ultrasonic/<action>')
api.add_resource(Entry, '/submit-entry/<action>')
api.add_resource(PlayGame, '/play-game/')
api.add_resource(Attempts, '/attempts/')
api.add_resource(Successes, '/successes/')
api.add_resource(HighScores, '/high-scores/')
api.add_resource(TimerText, '/timer-text/')
