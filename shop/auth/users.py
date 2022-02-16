from flask import render_template, url_for, redirect, session, request
from shop.models import User, db
from shop.auth.form import LogIn, Registr
from . import auth


@auth.route('/auth/<name>')
def user():
    user = User.query.filter(User.id == session['user_id'])
    return render_template('auth/user.html', name=user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('auth.login'))

    login = LogIn()

    if request.method == "POST":
        if not login.validate_on_submit():
            return render_template('auth/login.html', login=login)

        user = User.query.filter(User.email == login.email.data).first()
        if not user or user.pasword_validation(login.password.data):
            login.email.errors.append('Неверное имя или пароль')
        else:
            session['user_id'] = user.id
            session['email'] = login.email
            return redirect(url_for('auth.user'))
    return render_template('auth/login.html', login=login)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    register = Registr()
    if register.validate_on_submit():
        users = User.query.filter_by(email=register.email.data).first()
        if users is None:
            users = User(email=register.email.data, name=register.name.data, surname=register.surname.data,
                         password=register.password2.data)
            db.session.add(users)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            register.email.errors = ['Пользователь с такой почтой уже зарегестрирован']

    return render_template('auth/registration.html', register=register)
