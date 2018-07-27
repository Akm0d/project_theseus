#!/usr/bin/env python3
import logging
from argparse import ArgumentParser
from logging.handlers import RotatingFileHandler
from multiprocessing import Process, Queue
from os import path

import globals
from WebApp import app
from game.logic import Logic

log = logging.getLogger()
log_dir = path.dirname(__file__)

if not log_dir:
    log_dir = "."

if __name__ == '__main__':
    # Parse command line arguments
    args = ArgumentParser()
    args.add_argument("--debug", action="store_true")
    args.add_argument("--log-level", type=int, default=logging.INFO)

    opts = args.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO, handlers=[
        RotatingFileHandler("{}/{}.log".format(log_dir, __file__.split('/')[-1][:-3]), maxBytes=1280000, backupCount=1),
    ], format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s")

    stream = logging.StreamHandler()
    stream.setLevel(opts.log_level)
    stream.setFormatter(logging.Formatter("[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s"))
    logging.getLogger("apscheduler").setLevel(opts.log_level)
    logging.getLogger("apscheduler").propagate = False
    log.addHandler(stream)

    # Access ComQueue singleton
    q = globals.ComQueue()

    # Set up communications queue
    procComQueue = Queue()
    q.setComQueue(procComQueue)

    # Create the gameLogic Process
    gameLogic = Process(target=Logic().run, args=[procComQueue])
    gameLogic.start()

    # Run the Flask server here in the parent
    app.run(debug=False, host="::", port=5000)

    # Wait for the gameLogic process to finish. Prevents Zombie processes
    gameLogic.join()

