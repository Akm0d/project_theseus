#!/usr/bin/env python3
import os

if __name__ == '__main__':
    if not os.fork():
        from game.logic import Logic

        Logic().run()
    else:
        from WebApp import app

        app.run(debug=False, host="127.0.0.1", port=5000)
