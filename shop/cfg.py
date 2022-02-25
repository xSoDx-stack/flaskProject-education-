from os import getenv, environ


class Configuration:
    DEBUG = 'True'
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    database_path = getenv('DATABASE_URL')
    if database_path.startswith('postgres://'):                                     # This config renaming data base linck,
        database_path = database_path.replace('postgres://', 'postgresql://', 1)    # on the cloud platform PaaS Heroku
    SQLALCHEMY_DATABASE_URI = database_path
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '587'
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_DEBUG = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
