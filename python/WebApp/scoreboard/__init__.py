from flask import current_app as app, render_template, request, redirect, jsonify, url_for, Blueprint, \
    abort, render_template_string, send_file
from WebApp.scoreboard.database import init, insert

init() #create database if none exists

scoreboard = Blueprint('scoreboard', __name__)

@scoreboard.route('/scoreboard', methods=['GET'])
def admin_view():
    return render_template("scoreboard.html")
