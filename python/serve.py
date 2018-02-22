#!/usr/bin/env python3
from flask_apscheduler import APScheduler
from game.logic import Logic
from WebApp import app

app.run(debug=True, threaded=True, host="127.0.0.1", port=5000)

app.scheduler = APScheduler(app=app, scheduler=Logic())
app.scheduler.start()
