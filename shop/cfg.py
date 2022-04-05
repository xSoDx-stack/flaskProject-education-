from os import getenv


class ConfigurationRegisterable:
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = True
    SECURITY_EMAIL_SUBJECT_REGISTER = "Подтверждение регистрации"
    SECURITY_CONFIRMABLE = True
    SECURITY_CONFIRM_EMAIL_WITHIN = 2
    SECURITY_UNIFIED_SIGNIN = False
    SECURITY_EMAIL_SENDER = getenv('MAIL_USERNAME')
    SEND_REGISTER_EMAIL = True


class ConfigurationMail:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '587'
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_DEBUG = True
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')


class ConfigurationReCaptcha:
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = getenv('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = getenv('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}


class ConfigurationDB:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    database_path = getenv('DATABASE_URL')
    if database_path.startswith('postgres://'):  # This config renaming data base linck,
        database_path = database_path.replace('postgres://', 'postgresql://', 1)  # on the cloud platform PaaS Heroku
    SQLALCHEMY_DATABASE_URI = database_path


class Configuration(ConfigurationMail, ConfigurationReCaptcha, ConfigurationDB, ConfigurationRegisterable):
    DEBUG = 'True'
    SECRET_KEY = getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = getenv('SECURITY_PASSWORD_SALT')
    SECURITY_PASSWORD_HASH = 'bcrypt'  # bcrypt, argon2, sha512_crypt, or pbkdf2_sha512.
    SECURITY_TRACKABLE = True
