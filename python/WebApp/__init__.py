from flask import Flask

from WebApp.admin import admin
from WebApp.base import base
from WebApp.scoreboard import scoreboard
from WebApp.timer import timer

config = 'WebApp.config.Config'

app = Flask(__name__)
app.config.from_object(config)

# TODO init database


app.register_blueprint(admin)
app.register_blueprint(base)
app.register_blueprint(scoreboard)
app.register_blueprint(timer)
