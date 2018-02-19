from exrex import getone as regex2str
from flask import current_app as app, render_template, request, redirect, jsonify, url_for, Blueprint, \
    abort, render_template_string, send_file
from flask_restful import Api, Resource
from random import choice
from threading import Lock

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

admin = Blueprint('admin', __name__, url_prefix='/admin')
restful = Api(admin)


@admin.route('/', methods=['GET'])
def admin_view():
    return render_template("admin.html")


@restful.resource('/keycode/<code>')
class Keypad(Resource):
    def get(self, code: str):
        if not code == "status":
            # TODO Tell the listener to expect the given code on the keypad
            logger.debug("Setting new keypad code: {}".format(code))

        # TODO get the keycode from the Listner
        return {"status": regex2str("[a-f0-9]{3}" if code == "status" else code)}


@restful.resource('/rgb_select/<color>')
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


@restful.resource('/solenoid/<action>')
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


@restful.resource('/timer/<action>')
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


@restful.resource('/tripwire/<name>/<action>')
class Tripwire(Resource):
    def get(self, name: str, action: str):
        toggle = action == "toggle"
        logger.debug("Tripwire {}".format(name))
        if toggle:
            # TODO toggle this specific tripwire
            pass

        # TODO get the status of the tripwire.  Return green if enabled, else white
        return {"color": choice(["red", ""])}


@restful.resource('/tripwire/all/<action>')
class TripwireAll(Resource):
    def get(self, action):
        toggle = action == "toggle"
        # TODO if at least one tripwire is on, turn them all off.  If all of them are off, then randomize or turn all on
        status = dict()
        for i in range(1, 7):
            # TODO get the status of each tripwire.  Is it on or off?
            status[i] = choice(["red", ""])
        return status


@restful.resource('/tripwire/randomize')
class Randomize(Resource):
    def get(self):
        # TODO send a request to randomize the order of the lasers then return the status of all of them
        return dict()


@restful.resource('/ultrasonic/<action>')
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
