from flask import Flask
from WebApp.admin import admin
from WebApp.api import resource, scoreboard, base
from WebApp.timer import timer
from game.database import Database

config = 'WebApp.config.Config'

app = Flask(__name__)
app.config.from_object(config)

app.db = Database()
app.register_blueprint(admin)
app.register_blueprint(base)
app.register_blueprint(resource)
app.register_blueprint(scoreboard)
app.register_blueprint(timer)
