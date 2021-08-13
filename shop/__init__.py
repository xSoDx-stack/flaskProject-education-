from flask import Flask

from shop.cfg import Configuration
from shop.models import db

# from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)
# migrate = Migrate(app, db)

from shop.view import *


