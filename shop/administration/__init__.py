from flask import Blueprint

admin = Blueprint('admin', __name__)

from shop.administration import admins
