from flask import Blueprint

auth = Blueprint('auth', __name__)

from shop.auth import users
