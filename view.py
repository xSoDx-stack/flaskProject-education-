from main import app
from flask import render_template
from form import LogIn

@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_not_found(e):
    return render_template('500.html'), 500


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/login')
def login():
    login = LogIn()
    return render_template('login.html', login=login)


