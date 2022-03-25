from os import getenv


class ConfigurationMail:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '587'
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_DEBUG = True
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')


class ConfigurationReCaptcha:
    RECAPTCHA_ENABLED = True
    RECAPTCHA_SITE_KEY = getenv('RECAPTCHA_SITE_KEY')
    RECAPTCHA_SECRET_KEY = getenv('RECAPTCHA_SECRET_KEY')
    RECAPTCHA_THEME = 'dark'
    RECAPTCHA_TYPE = 'image'
    RECAPTCHA_SIZE = 'normal'
    RECAPTCHA_RTABINDEX = 10


class ConfigurationDB:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    database_path = getenv('DATABASE_URL')
    if database_path.startswith('postgres://'):  # This config renaming data base linck,
        database_path = database_path.replace('postgres://', 'postgresql://', 1)  # on the cloud platform PaaS Heroku
    SQLALCHEMY_DATABASE_URI = database_path


class Configuration(ConfigurationMail, ConfigurationReCaptcha, ConfigurationDB):
    DEBUG = 'True'
    SECRET_KEY = getenv('SECRET_KEY')





