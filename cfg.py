from os import getenv
class Configuration:
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = getenv('URL_For_Database')
    SQLALCHEMY_TRACK_MODIFICATIONS = False