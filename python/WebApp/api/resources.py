import random
from logging.handlers import RotatingFileHandler

import logging
from flask_restful import Resource
from game.logic import Logic

log = logging.getLogger(__name__)
handler = RotatingFileHandler("{}.log".format(__name__), maxBytes=1280000, backupCount=1)
handler.setFormatter(logging.Formatter("[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s"))
handler.setLevel(logging.DEBUG)
log.addHandler(handler)

state = Logic()


class Keypad(Resource):
    def get(self):
        return {"status": state.keypad_code}

    def put(self, code):
        state.keypad_code = code
        return {"status": state.keypad_code}


class RGB(Resource):
    options = ["black", "red", "green", "blue"]

    def get(self, color: str):
        if not color == "status":
            # TODO Send a request to the Listener that changes the color of the RGB
            log.debug("selecting '{}'".format(color))
        # TODO Get the actual color of the rgb from the listener
        if color == "status":
            color = random.choice(self.options)

        # The javascript needs the index in the selection wheel that matches the given color
        return {"status": self.options.index(color), "color": ""
                if color == "black" else "lawngreen"
                if color == "green" else "deepskyblue"
                if color == "blue" else color
                }


class Solenoid(Resource):
    def __init__(self):
        self.enabled = True

    def get(self, action: str):
        if action == "toggle":
            log.debug("Toggling the solenoid")
            # TODO make a request to the listener.  Ask to change the enabled state of the solenoid
            pass

        # TODO get the state of the solenoid from the listener instead of a random choice
        return {"status": random.choice(["Open", "Closed"])}


class Timer(Resource):
    def __init__(self):
        self.enabled = True

    def get(self, action: str):
        if action == "toggle":
            log.debug("Toggling the timer")
            # TODO make a request to the listener.  Ask to change the enabled state of the timer

        # TODO get the state of the timer from the listener instead of a random choice
        return {"status": random.choice(["Reset", "Start"])}


class Tripwire(Resource):
    def get(self, name: str, action: str):
        toggle = action == "toggle"
        log.debug("Tripwire {}".format(name))
        if toggle:
            # TODO toggle this specific tripwire
            pass

        # TODO get the status of the tripwire.  Return green if enabled, else white
        return {"color": random.choice(["#DC3545", ""])}


class TripwireAll(Resource):
    def get(self, action):
        toggle = action == "toggle"
        # TODO if at least one tripwire is on, turn them all off.  If all of them are off, then randomize or turn all on
        status = dict()
        for i in range(1, 7):
            # TODO get the status of each tripwire.  Is it on or off?
            status[i] = random.choice(["#DC3545", ""])
        return status


class Randomize(Resource):
    def get(self):
        # TODO send a request to randomize the order of the lasers then return the status of all of them
        return dict()


class Ultrasonic(Resource):
    def __init__(self):
        self.enabled = True

    def get(self, action: str):
        if action == "toggle":
            log.debug("Toggling the ultrasonic sensor")
            # TODO make a request to the listener.  Ask to change the enabled state of ultrasonic
            pass

        # TODO get the state of the ultrasonic sensor instead of a random choice
        return {"status": random.choice(["Enabled", "Disabled"])}


class Team(Resource):
    def get(self):
        return {"status": state.team}

    def put(self, name):
        state.team = name
        return {"status": state.team}


class Attempts(Resource):
    def get(self):
        return {"attempts": 100}


class Successes(Resource):
    def get(self):
        return {"successes": 5}


class HighScores(Resource):
    def get(self):
        # TODO return top 5 unique scores from database
        return {"team1": {"name": "person", "time": "00:59"},
                "team2": {"name": "person2","time": "01:25"},
                "team3": {"name": "person3","time": "02:25"},
                "team4": {"name": "person4","time": "03:25"},
                "team5": {"name": "person5","time": "04:25"}
                }


class TimerText(Resource):
    def get(self):
        return {"timer": "04:55"}
