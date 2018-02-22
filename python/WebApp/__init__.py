from flask import Flask

config = 'WebApp.config.Config'

app = Flask(__name__)
app.config.from_object(config)

# TODO init database

from WebApp.admin import admin
from WebApp.base import base
from WebApp.register import register
from WebApp.scoreboard import scoreboard
from WebApp.timer import timer
from . import api

app.register_blueprint(admin)
app.register_blueprint(base)
app.register_blueprint(register)
app.register_blueprint(scoreboard)
app.register_blueprint(timer)
