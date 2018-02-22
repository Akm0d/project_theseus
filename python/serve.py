#!/usr/bin/env python3
import os

if __name__ == '__main__':
    if os.fork() == 0:
        from game.logic import Logic
        Logic().run()
    else:
        from WebApp import app
        app.run(host="127.0.0.1", port=5000)
