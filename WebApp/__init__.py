from flask import Flask, Blueprint, render_template, url_for

from WebApp.api import resource
from game.database import Database

config = 'WebApp.config.Config'

app = Flask(__name__)
app.config.from_object(config)

admin = Blueprint('admin', __name__, url_prefix='/admin')
base = Blueprint('base', __name__)
timer = Blueprint('timer', __name__)


@admin.route('/', methods=['GET'])
def admin_view():
    return render_template("admin.html")


@base.route('/', methods=['GET'])
def base_view():
    return render_template("index.html")


# TODO 404 not found and other error pages

@base.route('/favicon.ico', methods=['GET'])
def favicon():
    return url_for('static', filename='favicon.ico')


@timer.route('/timer', methods=['GET'])
def admin_view():
    return "TODO timer"


app.db = Database()
app.register_blueprint(admin)
app.register_blueprint(base)
app.register_blueprint(resource)
