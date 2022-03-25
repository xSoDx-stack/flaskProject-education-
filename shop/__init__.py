from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from shop.cfg import Configuration
from flask_mail import Mail
from flask_migrate import Migrate
from flask_recaptcha import ReCaptcha

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
recaptcha = ReCaptcha()


def create_app(config_class=Configuration):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    recaptcha.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from shop.auth import auth
    from shop.errors import error_bp
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(error_bp)
    return app


app = create_app()
from shop.view import *
