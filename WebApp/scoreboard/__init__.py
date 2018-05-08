from flask import render_template, Blueprint

scoreboard = Blueprint('scoreboard', __name__)


@scoreboard.route('/scoreboard', methods=['GET'])
def admin_view():
    return render_template("scoreboard.html")
