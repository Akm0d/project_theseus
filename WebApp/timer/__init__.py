from flask import current_app as app, render_template, request, redirect, jsonify, url_for, Blueprint, \
    abort, render_template_string, send_file

timer = Blueprint('timer', __name__)


@timer.route('/timer', methods=['GET'])
def admin_view():
    return "TODO timer"
