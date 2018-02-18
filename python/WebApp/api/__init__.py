from flask import Blueprint, current_app as app, request
from flask_restful import Api, Resource

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint)


# TODO make 'ultrasonic' a <device> or <sensor> variable that can enable/disable any device
@api.resource('/ultrasonic/<action>')
class Ultrasonic(Resource):
    def __init__(self):
        self.enabled = True

    def get(self, action=None):
        if action == "toggle":
            # TODO make a request to the listener.  Ask to change the enabled state of ultrasonic
            pass

        # TODO get the state of the ultrasonic sensor
        from random import choice
        enabled = choice([True, False])

        return {"status": "Enabled" if enabled else "Disabled"}

