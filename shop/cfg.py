from os import getenv

class Configuration:
    DEBUG = 'True'
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
