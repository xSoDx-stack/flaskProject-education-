from flask import render_template, url_for, redirect, session, request
from shop import db
from shop.models import User
from shop.auth.form import LogIn, Registr, RequestResetPassword, ResetPassword
from . import auth
from .email import send_password_reset_email


@auth.route('/user/<name>')
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
            login.email.errors = ['Неверное имя или пароль']
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


@auth.route('/reset_password', methods=['GET', 'POST'])
def send_password_reset():
    res_pass = RequestResetPassword()
    if res_pass.validate_on_submit():
        mail = User.query.filter_by(email=res_pass.email.data).first()
        if mail:
            send_password_reset_email(mail)
            return render_template('auth/info_pass_res.html')
        else:
            res_pass.email.errors = ['Пользователя с такой почтой не найдено']
    return render_template('auth/send_password_reset.html', res_pass=res_pass)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPassword()
    if form.validate_on_submit():
        user.password = form.password2.data
        db.session.add(user)
        db.session.commit()
        return render_template('auth/pass_successfully_changed.html')
    elif form.validate_on_submit():
        form.password2.errors = ['Пароли не совпадают !']
    return render_template('auth/reset_password.html', form=form)
