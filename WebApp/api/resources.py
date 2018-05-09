import random
from logging.handlers import RotatingFileHandler

import logging
from flask_restful import Resource
from game.database import Database
from game.logic import Logic
from game.constants import STATE, COMMUNICATION, SOLENOID_STATE, JSCom, TIME_GIVEN, ULTRASONIC_STATE
import datetime

from globals import ComQueue

log = logging.getLogger(__name__)
handler = RotatingFileHandler("{}.log".format(__name__), maxBytes=1280000, backupCount=1)
handler.setFormatter(logging.Formatter("[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s"))
handler.setLevel(logging.ERROR)
log.addHandler(handler)

state = Logic()

start_time = None
end_time = None


def getState():
    ComQueue().getComQueue().put([COMMUNICATION.GET_STATE])
    while (1):
        if not ComQueue().getComQueue().empty():
            object = ComQueue().getComQueue().get()
            if object[0] == COMMUNICATION.SENT_STATE:
                return object[1]
            else:
                # Not what we are looking for, put it back
                ComQueue().getComQueue().put(object)
        else:
            # queue is empty
            pass


class Keypad(Resource):
    def get(self):
        ComQueue().getComQueue().put([COMMUNICATION.GET_CODE])
        while (1):
            if not ComQueue().getComQueue().empty():
                object = ComQueue().getComQueue().get()
                if object[0] == COMMUNICATION.SENT_CODE:
                    return {"status": object[1]}
                else:
                    # Not for me
                    ComQueue().getComQueue().put(object)
            else:
                # Queue is empty
                pass

    def put(self, code):
        ComQueue().getComQueue().put([COMMUNICATION.SET_CODE, code])
        # No need to query what it will be as I know
        return {"status": code}


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
    # REMOVED BECAUSE WE NOW GET THIS FROM LOGIC
    # def __init__(self):
    #     self.enabled = True

    def get(self, action: str):
        status = "unlocked"
        if action == "toggle":
            log.debug("Toggling the solenoid")
            ComQueue().getComQueue().put([COMMUNICATION.TOGGLE_SOLENOID])
            toggleComplete = False
            while not toggleComplete:
                if not ComQueue().getComQueue().empty():
                    object = ComQueue().getComQueue().get()
                    if object[0] == COMMUNICATION.SENT_SOLENOID_STATUS:
                        status = object[1]
                        toggleComplete = True  # Leave while
                    else:
                        # Not what we are looking for, put it back
                        ComQueue().getComQueue().put(object)
                else:
                    # queue is empty
                    pass
        else:
            # Get solenoid status
            ComQueue().getComQueue().put([COMMUNICATION.SOLENOID_STATUS])
            statusComplete = False
            while (not statusComplete):
                if not ComQueue().getComQueue().empty():
                    object = ComQueue().getComQueue().get()
                    if object[0] == COMMUNICATION.SENT_SOLENOID_STATUS:
                        status = object[1]
                        statusComplete = True
                    else:
                        ComQueue().getComQueue().put(object)
                else:
                    # queue is empty
                    pass

        if status is SOLENOID_STATE.LOCKED:
            return {"status": SOLENOID_STATE.LOCKED.value}
        elif status is SOLENOID_STATE.UNLOCKED:
            return {"status": SOLENOID_STATE.UNLOCKED.value}


class Timer(Resource):
    def __init__(self):
        self.enabled = True

    def get(self, action: str):
        global start_time
        state = getState()

        if action == "toggle":
            if state is STATE.WAIT:
                # Waiting to begin
                start_time = datetime.datetime.now()
                ComQueue().getComQueue().put([COMMUNICATION.START_GAME])
                state = STATE.RUNNING
            elif state is STATE.RUNNING:
                end_time = datetime.datetime.now()
                ComQueue().getComQueue().put([COMMUNICATION.RESET_GAME])
                state = STATE.WAIT
            else:
                ComQueue().getComQueue().put([COMMUNICATION.RESET_GAME])
                state = STATE.WAIT

        # Based on state, send a specific code
        if state is STATE.RUNNING:
            return {"status": JSCom.RESET_BUTTON.value}
        else:
            return {"status": JSCom.START_BUTTON.value}


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
        status = ULTRASONIC_STATE.DISABLED
        if action == "toggle":
            log.debug("Toggling the ultrasonic")
            ComQueue().getComQueue().put([COMMUNICATION.TOGGLE_ULTRASONIC])
            toggleComplete = False
            while (not toggleComplete):
                if not ComQueue().getComQueue().empty():
                    object = ComQueue().getComQueue().get()
                    if (object[0] == COMMUNICATION.SENT_ULTRASONIC):
                        status = object[1]
                        toggleComplete = True  # Leave while
                    else:
                        # Not what we are looking for, put it back
                        ComQueue().getComQueue().put(object)
                else:
                    # queue is empty
                    pass
        else:
            # Get solenoid status
            ComQueue().getComQueue().put([COMMUNICATION.GET_ULTRASONIC])
            statusComplete = False
            while (not statusComplete):
                if not ComQueue().getComQueue().empty():
                    object = ComQueue().getComQueue().get()
                    if (object[0] == COMMUNICATION.SENT_ULTRASONIC):
                        status = object[1]
                        statusComplete = True
                    else:
                        ComQueue().getComQueue().put(object)
                else:
                    # queue is empty
                    pass

        if status is ULTRASONIC_STATE.DISABLED:
            return {"status": ULTRASONIC_STATE.DISABLED.value}
        elif status is ULTRASONIC_STATE.ENABLED:
            return {"status": ULTRASONIC_STATE.ENABLED.value}


class Entry(Resource):
    def post(self, action: str):
        if action is not "":
            # Make a new entry for this team
            # TODO: Create a new row in the database with the current timer and with action team name
            log.info("Added team {} to the database as a team to successfully complete the box.".format(action))
        else:
            pass  # Do nothing, they didn't put a team.
        return dict()


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
    def __init__(self):
        self.db = Database()

    def get(self):
        # TODO return top 5 unique scores from database
        scores = self.db.get_rows(success=True)
        scores.sort(key=lambda x: x.time, reverse=False)
        return {
            "team{}".format(i): {"name": "{}".format(row.name), "time": "{}".format(row.time)} for i, row in
        enumerate(scores)
        }


class TimerText(Resource):
    def get(self):
        global start_time
        state = getState()
        if state == STATE.WAIT:
            return {"timer": "03:00"}
        elif state == STATE.RUNNING:
            newDatetime = datetime.datetime.now() - start_time
            seconds = TIME_GIVEN - newDatetime.seconds
            minutes = seconds // 60
            secondsToPrint = seconds - minutes * 60
            if seconds <= 0:
                # Player ran out of time
                ComQueue().getComQueue().put([COMMUNICATION.KILL_PLAYER])
                return {"timer": "DEAD"}
            else:
                return {"timer": "{}:{:2}".format(minutes, secondsToPrint)}
