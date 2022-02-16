from flask import Blueprint

error_bp = Blueprint('errors', __name__)

from shop.errors import errors
