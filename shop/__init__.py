from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from shop.cfg import Configuration
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from shop.view import *


