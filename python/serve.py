#!/usr/bin/env python3
import os
import argparse

parser = argparse.ArgumentParser(description='Defusal Station web server')
parser.add_argument('--debug', action="store_true", help="Debug Level")
args = parser.parse_args()

if __name__ == '__main__':
    if os.fork() == 0:
        from game.logic import Logic
        Logic().run()
    else:
        from WebApp import app
        app.run(debug=args.debug, host="127.0.0.1", port=5000)
