from flask import current_app as app, render_template, request, redirect, jsonify, url_for, Blueprint, \
    abort, render_template_string, send_file

register = Blueprint('register', __name__)


@register.route('/register', methods=['GET'])
def admin_view():
    return "TODO Register"
