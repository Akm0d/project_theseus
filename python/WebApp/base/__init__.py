from flask import current_app as app, render_template, request, redirect, jsonify, url_for, Blueprint, \
    abort, render_template_string, send_file

base = Blueprint('base', __name__, template_folder='WebApp/frontend/templates')


@base.route('/', methods=['GET'])
def admin_view():
    return render_template("index.html")

# TODO 404 not found and other error pages

# TODO favicon
