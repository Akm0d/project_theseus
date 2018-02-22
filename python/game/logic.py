from apscheduler.schedulers.background import BackgroundScheduler


class Logic(BackgroundScheduler):
    def __init__(self):
        super().__init__(timezone="MST")
        # TODO trigger immediately after previous instance ends
        self.add_job(self.loop, max_instances=1, id="hash_crack_king", trigger='interval', seconds=1)

    def loop(self):
        # TODO this is the game loop that polls I2C and tracks the state of the game
        pass
