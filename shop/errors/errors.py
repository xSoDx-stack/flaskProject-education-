from flask import render_template
from . import error_bp as error


@error.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@error.app_errorhandler(500)
def server_not_found(e):
    return render_template('error/500.html'), 500
