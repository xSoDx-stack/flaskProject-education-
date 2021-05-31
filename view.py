from main import app
from app import db
from flask import render_template, redirect, url_for, session, request
from form import LogIn, Registr
from model import Role, User

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


@app.route('/login', methods = ['GET', 'POST'])
def login():
    login = LogIn()
    name = None
    if login.validate_on_submit():
        session['name'] = login.email.data
        return  redirect(url_for('index'))
    return render_template('login.html', login=login, name=session.get('name'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    register = Registr()
    if register.validate_on_submit():
        user = User.query.filter_by(email=register.email.data).first()
        if user is None:
            user = User(email=register.email.data, name=register.name.data, surname=register.surname.data, password=register.password.data)
            db.session.add(user)
            session['known'] = False
            db.session.commit()
            print('Выполнилось')
        else:
            session['known'] = True
            session['email'] = register.email.data
            session['name'] = register.name.data
            session['surname'] = register.surname.data
            register.email.data = ''
            print('Ошибка')
            return redirect(url_for('register'))

    return render_template('registration.html', register=register)



