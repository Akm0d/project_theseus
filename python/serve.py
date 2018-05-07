#!/usr/bin/env python3
from game.logic import Logic
from logging.handlers import RotatingFileHandler
from WebApp import app
from argparse import ArgumentParser
import logging
import multiprocessing as mp
import globals
from game.constants import LOGGING_LEVEL

logger = logging.getLogger()

if __name__ == '__main__':
    args = ArgumentParser()
    args.add_argument("--mock", action="store_true")
    args.add_argument("--debug", action="store_true")
    args.add_argument("--log-level", type=int, default=logging.INFO)
    opts = args.parse_args()

    # Setup logger
    print("Setting log level to {}".format(opts.log_level))
    logger.setLevel(opts.log_level)
    handler = RotatingFileHandler("webapp.log", maxBytes=1280000, backupCount=1)
    handler.setFormatter(logging.Formatter("[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s"))
    handler.setLevel(opts.log_level)
    logger.addHandler(handler)

    # Access ComQueue singleton
    q = globals.ComQueue()

    # Set up communications queue
    procComQueue = mp.Queue()
    q.setComQueue(procComQueue) # Set the ComQueue

    # Create the gameLogic Process
    gameLogic = mp.Process(target=Logic().run, args=(procComQueue, opts.mock, opts.debug))

    # Start the Logic Process by forking (default start() behavior for unix)
    gameLogic.start()

    # Run the Flask server here in the parent
    app.run(debug=False, host="0.0.0.0", port=5000)

    # Wait for the gameLogic process to finish. Prevents Zombie processes
    gameLogic.join()
