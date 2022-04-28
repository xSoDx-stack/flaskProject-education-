from os import getenv


class ConfigurationRBAC:
    RBAC_USE_WHITE = True


class ConfigurationFlaskLogin(ConfigurationRBAC):
    REMEMBER_COOKIE_DURATION = 86400
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = True


class ConfigurationSesion(ConfigurationFlaskLogin):
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = 7200


class ConfigurationMail(ConfigurationSesion):
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '587'
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_DEBUG = True
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')


class ConfigurationReCaptcha(ConfigurationMail):
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = getenv('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = getenv('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}


class ConfigurationDB(ConfigurationReCaptcha):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    database_path = 'postgres://txiyqdeiddgegi:636272b7dd8f8c55d201bc871c03d35c1e0017faab90ea7ed843f4f304a9c14a@ec2-52-18-116-67.eu-west-1.compute.amazonaws.com:5432/d8i5rv1vejub8i'
    if database_path.startswith('postgres://'):  # This config renaming data base linc,
        database_path = database_path.replace('postgres://', 'postgresql://', 1)  # on the cloud platform PaaS Heroku
    SQLALCHEMY_DATABASE_URI = database_path


class Configuration(ConfigurationDB):
    DEBUG = 'True'
    SECRET_KEY = getenv('SECRET_KEY')
    TOKEN_SECRET_KEY = 'TOKEN_SECRET_KEY'
    TOKEN_SALT = 'TOKEN_SALT'
    FLASK_ADMIN_SWATCH = 'flatly'

