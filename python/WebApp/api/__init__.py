from flask import Blueprint, current_app as app, request
from flask_restful import Api, Resource
from random import choice

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)


@api.resource('/rgb_select/<color>')
class RGB(Resource):
    options = ["black", "red", "green", "blue"]

    def get(self, color: str):
        if not color == "status":
            # TODO Send a request to the Listener that changes the color of the RGB
            logger.debug("selecting '{}'".format(color))
        # TODO Get the actual color of the rgb from the listener
        if color == "status":
            color = choice(self.options)

        # The javascript needs the index in the selection wheel that matches the given color
        return {"status": self.options.index(color), "color": "" if color == "black" else color}


@api.resource('/solenoid/<action>')
class Solenoid(Resource):
    def __init__(self):
        self.enabled = True

    def get(self, action: str):
        if action == "toggle":
            logger.debug("Toggling the solenoid")
            # TODO make a request to the listener.  Ask to change the enabled state of the solenoid
            pass

        # TODO get the state of the solenoid from the listener instead of a random choice
        return {"status": choice(["Open", "Closed"])}


@api.resource('/timer/<action>')
class Timer(Resource):
    def __init__(self):
        self.enabled = True

    def get(self, action: str):
        if action == "toggle":
            logger.debug("Toggling the timer")
            # TODO make a request to the listener.  Ask to change the enabled state of the timer
            pass

        # TODO get the state of the timer from the listener instead of a random choice
        return {"status": choice(["Reset", "Start"])}


@api.resource('/tripwire/<name>/<action>')
class Tripwire(Resource):
    def get(self, name: str, action: str):
        toggle = action == "toggle"
        logger.debug("Tripwire {}".format(name))
        if toggle:
            # TODO toggle this specific tripwire
            pass

        # TODO get the status of the tripwire.  Return green if enabled, else white
        return {"color": choice(["red", ""])}


@api.resource('/tripwire/all/<action>')
class TripwireAll(Resource):
    def get(self, action):
        toggle = action == "toggle"
        # TODO if at least one tripwire is on, turn them all off.  If all of them are off, then randomize or turn all on
        status = dict()
        for i in range(1, 7):
            # TODO get the status of each tripwire.  Is it on or off?
            status[i] = choice(["red", ""])
        return status


@api.resource('/tripwire/randomize')
class Randomize(Resource):
    def get(self):
        # TODO send a request to randomize the order of the lasers then return the status of all of them
        return dict()


@api.resource('/ultrasonic/<action>')
class Ultrasonic(Resource):
    def __init__(self):
        self.enabled = True

    def get(self, action: str):
        if action == "toggle":
            logger.debug("Toggling the ultrasonic sensor")
            # TODO make a request to the listener.  Ask to change the enabled state of ultrasonic
            pass

        # TODO get the state of the ultrasonic sensor instead of a random choice
        return {"status": choice(["Enabled", "Disabled"])}
