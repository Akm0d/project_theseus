from flask import Flask

from WebApp.api import resource, base, admin
from game.database import Database

config = 'WebApp.config.Config'

app = Flask(__name__)
app.config.from_object(config)

app.db = Database()
app.register_blueprint(admin)
app.register_blueprint(base)
app.register_blueprint(resource)
