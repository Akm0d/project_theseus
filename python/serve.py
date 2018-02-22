#!/usr/bin/env python3
import os
from logging.handlers import RotatingFileHandler
from flask import logging

logger = logging.getLogger()

if __name__ == '__main__':
    if not os.fork():
        from game.logic import Logic
        Logic().run()
    else:
        from WebApp import app
        handler = RotatingFileHandler("webapp.log", maxBytes=1280000, backupCount=1)
        handler.setFormatter(logging.Formatter("[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s"))
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        app.run(debug=False, host="127.0.0.1", port=5000)

