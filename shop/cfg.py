from os import getenv


class Configuration:
    DEBUG = 'True'
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    database_path = getenv('DATABASE_URL')
    if database_path.startswith('postgres://'):                                     # This config renaming data base linck,
        database_path = database_path.replace('postgres://', 'postgresql://', 1)    # on the cloud platform PaaS Heroku
    SQLALCHEMY_DATABASE_URI = database_path
