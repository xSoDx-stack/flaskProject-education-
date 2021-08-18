import re
from os import getenv

class Configuration:
    DEBUG = 'True'
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    database_path = getenv('DATABASE_URL')
    if database_path.startswith('postgres://'):
        database_path = database_path.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_path