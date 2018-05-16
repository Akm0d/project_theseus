#!/usr/bin/env python3
import logging
import multiprocessing as mp
from argparse import ArgumentParser
from logging.handlers import RotatingFileHandler
from os import path, mkdir

import globals
from WebApp import app
from game.logic import Logic
from qt.mock_box_ui import ApplicationWindow

log = logging.getLogger()
log_dir = path.dirname(__file__)

if __name__ == '__main__':
    # Parse command line arguments
    args = ArgumentParser()
    args.add_argument("--mock", action="store_true")
    args.add_argument("--debug", action="store_true")
    args.add_argument("--log-level", type=int, default=logging.INFO)

    opts = args.parse_args()

    # Configure logging
    if not path.exists(log_dir):
        mkdir(log_dir)
    logging.basicConfig(level=logging.INFO,  handlers=[
        RotatingFileHandler("{}/{}.log".format(log_dir, __file__.split('/')[-1][:-3]), maxBytes=1280000, backupCount=1),
    ], format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s")

    stream = logging.StreamHandler()
    stream.setLevel(opts.log_level)
    stream.setFormatter(logging.Formatter("[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s"))
    log.addHandler(stream)

    # Access ComQueue singleton
    q = globals.ComQueue()

    # Set up communications queue
    procComQueue = mp.Queue()
    q.setComQueue(procComQueue)

    # Create the gameLogic Process
    gameLogic = mp.Process(target=Logic().run, args=(procComQueue, opts.mock))

    # Start the Logic Process by forking (default start() behavior for unix)
    gameLogic.start()

    qt_app = None
    if opts.mock:
        # Start the gui the simulates the box
        print("starting app window")
        qt_app = mp.Process(target=ApplicationWindow.run)
        qt_app.start()

    # Run the Flask server here in the parent
    app.run(debug=False, host="0.0.0.0", port=5000)

    # Wait for the gameLogic process to finish. Prevents Zombie processes
    gameLogic.join()
    if qt_app is not None:
        qt_app.join()
