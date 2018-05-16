import logging

from flask_restful import Resource

from game.constants import STATE, INTERRUPT, SOLENOID_STATE, JSCom, ULTRASONIC_STATE, RGBColor
from game.database import Database
from game.logic import Logic
from globals import ComQueue

log = logging.getLogger(__name__)

logic = Logic()


class Keypad(Resource):
    def get(self):
        return {"status": str(hex(logic.keypad_code)[2:])}

    def put(self, code):
        logic.keypad_code = int("0x" + str(code), 16)
        return self.get()


class RGB(Resource):
    options = ["black", "red", "green", "blue"]

    def get(self):
        color = logic.rgb_color
        return {"status": self.options.index(color.value),
                "color": "" if color is RGBColor.BLANK else
                "lawngreen" if color is RGBColor.GREEN else
                "deepskyblue" if color is RGBColor.BLUE else
                color.value
                }

    def put(self, color: str):
        logic.rgb_color = RGBColor(color)
        return self.get()


class Solenoid(Resource):
    # REMOVED BECAUSE WE NOW GET THIS FROM LOGIC
    # def __init__(self):
    #     self.enabled = True

    def get(self, action: str):
        if action == "toggle":
            logic.solenoid = SOLENOID_STATE.UNLOCKED if logic.solenoid else SOLENOID_STATE.LOCKED
        return {"status": logic.solenoid.name.lower()}


class Timer(Resource):
    def __init__(self):
        self.enabled = True

    def get(self, action: str):
        if action == "toggle":
            ComQueue().getComQueue().put([INTERRUPT.TOGGLE_TIMER])

        return {"status": JSCom.RESET_BUTTON.value if logic.state is STATE.RUNNING else JSCom.START_BUTTON.value}


class Tripwire(Resource):
    def get(self, name: str or int, action: str):
        toggle = action == "toggle"
        log.debug("Tripwire {}".format(name))
        mask = 1 << int(name)
        if toggle:
            logic.lasers ^= mask
        return {"color": "#DC3545" if logic.lasers & mask else ""}


class TripwireAll(Resource):
    def get(self, action):
        toggle = action == "toggle"
        # if at least one tripwire is on, turn them all off.  If all of them are off, then randomize or turn all on
        if toggle:
            if logic.lasers:
                logic.lasers = 0x00
            else:
                logic.lasers = 0x7F
        status = dict()
        for i in range(1, 7):
            status[i] = Tripwire().get(i, "status")["color"]
        return status


class Randomize(Resource):
    def get(self):
        log.debug("Randomizing the lasers")
        logic.lasers = logic.random_laser_pattern()


class Ultrasonic(Resource):
    def __init__(self):
        self.enabled = True

    def get(self, action: str):
        if action == "toggle":
            log.debug("Toggling the ultrasonic")
            logic.ultrasonic = ULTRASONIC_STATE.DISABLED if logic.ultrasonic else ULTRASONIC_STATE.ENABLED
        return {"status": logic.ultrasonic.name.lower()}


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
    db = Database()

    def get(self):
        return {"status": logic.team}

    def put(self, name):
        logic.team = name
        return {"status": logic.team}


class Attempts(Resource):
    db = Database()

    def get(self):
        return {"attempts": len(self.db.get_rows())}


class Successes(Resource):
    db = Database()

    def get(self):
        return {"successes": len(self.db.get_rows(success=True))}


class HighScores(Resource):
    db = Database()

    def get(self):
        scores = self.db.get_rows(success=True)
        scores.sort(key=lambda x: x.time, reverse=False)
        return {
            "team{}".format(i + 1): {"name": "{}".format(row.name), "time": "{}".format(row.time)} for i, row in
            enumerate(scores)
        }


class TimerText(Resource):
    def get(self):
        return {"timer": logic.timer_text}
