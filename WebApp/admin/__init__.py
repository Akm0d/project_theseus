from flask import render_template, Blueprint

import logging

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/', methods=['GET'])
def admin_view():
    return render_template("admin.html")
