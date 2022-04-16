from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer, URLSafeSerializer
from shop.cfg import Configuration
from flask_mail import Mail
from flask_migrate import Migrate
import hashlib
from .utils import MRBAC


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()

serialize = URLSafeTimedSerializer(secret_key=Configuration.TOKEN_SECRET_KEY, salt=Configuration.TOKEN_SALT,
                                   signer_kwargs={"digest_method": hashlib.sha512})
ser_user = URLSafeSerializer(secret_key=Configuration.TOKEN_SECRET_KEY, salt=Configuration.TOKEN_SALT,
                             signer_kwargs={"digest_method": hashlib.sha512})


def create_app(config_class=Configuration):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = 'strong'
    from shop.auth import auth
    from shop.admin import admin
    from shop.errors import error_bp
    from shop.seller import seller
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_perefix='/admin')
    app.register_blueprint(seller, url_prefix='/seller')
    app.register_blueprint(error_bp)
    return app


app = create_app()
from shop.view import *
