from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from shop.cfg import Configuration
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)

from shop.errors import error_bp
from shop.auth import auth
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(error_bp)

migrate = Migrate(app, db)

from shop.view import *
