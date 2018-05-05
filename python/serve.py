#!/usr/bin/env python3
from game.logic import Logic
from logging.handlers import RotatingFileHandler
from WebApp import app
from argparse import ArgumentParser
import logging
import os

logger = logging.getLogger()

if __name__ == '__main__':
    args = ArgumentParser()
    args.add_argument("--mock", action="store_true")
    opts = args.parse_args()
    handler = RotatingFileHandler("webapp.log", maxBytes=1280000, backupCount=1)
    handler.setFormatter(logging.Formatter("[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s"))
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    if os.fork():
        Logic().run(mock=opts.mock)
    else:
        app.run(debug=False, host="0.0.0.0", port=5000)
