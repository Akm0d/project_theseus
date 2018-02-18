from flask import current_app as app, render_template, request, redirect, jsonify, url_for, Blueprint, \
    abort, render_template_string, send_file

base = Blueprint('base', __name__)


@base.route('/', methods=['GET'])
def base_view():
    return render_template("index.html")


# TODO 404 not found and other error pages

@base.route('/favicon.ico', methods=['GET'])
def favicon():
    return url_for('static', filename='favicon.ico')
