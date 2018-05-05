from enum import Enum

# What are the logical states for the state machine
class STATES(Enum):
    # INIT event goes to WAIT
    WAIT = "wait"
    # WAIT goes to RUNNING on PLAY
    RUNNING = "run"
    # RUNNING goes to either WIN or EXPLODE depending on if
    # It recieves a SUCCESS or a FAILURE
    WIN = "win"
    EXPLODE = "explode"
    # EXPLODE and WIN go to WAIT on RESET

# What are the events that trigger transitions between each state
class EVENTS(Enum):
    INIT = "init"
    PLAY = "play"
    SUCCESS = "success"
    FAILURE = "failure"
    RESET = "reset"
