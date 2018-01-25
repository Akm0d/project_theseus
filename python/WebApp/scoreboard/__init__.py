from flask import current_app as app, render_template, request, redirect, jsonify, url_for, Blueprint, \
    abort, render_template_string, send_file

scoreboard = Blueprint('scoreboard', __name__)


@scoreboard.route('/scoreboard', methods=['GET'])
def admin_view():
    return "TODO Scoreboard"
