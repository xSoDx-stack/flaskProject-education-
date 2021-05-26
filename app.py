from flask import Flask
from os import getenv
from sys import  exit

app = Flask(__name__)
secret_key = getenv('SECRET_KEY')
app.config['SECRET_KEY'] = secret_key



