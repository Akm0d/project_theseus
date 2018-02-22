from time import sleep


class Logic:
    def __init__(self):
        # TODO have a bunch of properties that change the game state and read the game state from the database
        pass

    def run(self):
        while True:
            # TODO this is the game loop that polls I2C and tracks the state of the game
            sleep(1)
