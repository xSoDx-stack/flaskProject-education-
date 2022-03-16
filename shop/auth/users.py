from flask import render_template, url_for, redirect, session, request
from shop import db
from shop.auth.form import LogIn, Registr, RequestResetPassword, ResetPassword
from shop.models import User
from . import auth
from .email import send_password_reset_email


@auth.route('/register', methods=['GET', 'POST'])
def register():
    _register = Registr()
    if _register.validate_on_submit():
        users = User.query.filter_by(email=_register.email.data).first()
        if not users:
            users = User(email=_register.email.data, name=_register.name.data, surname=_register.surname.data,
                         password=_register.password2.data)
            db.session.add(users)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            _register.email.errors = ['Пользователь с такой почтой уже зарегистрирован']
    return render_template('auth/registration.html', register=_register)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if session.get('user_id'):
        return redirect(url_for('auth.my'))
    else:
        _login = LogIn()
        if request.method == 'POST':

            if _login.validate_on_submit():
                user = User.query.filter(User.email == _login.email.data).first()
                if user:
                    if user.password_validation(_login.password.data):
                        session['user_id'] = user.id
                        session['email'] = user.email
                        session['name'] = user.name
                        return redirect(url_for('auth.my'))
                    else:
                        _login.email.errors = 'Неверно введена почта или пароль'
                else:
                    _login.email.errors = 'Неверно введена почта или пароль'
        return render_template('auth/login.html', login=_login)


@auth.route('/main/my')
def my():
    if session.get('user_id'):
        name = session['name']
    else:
        return redirect((url_for('auth.login')))
    return render_template('auth/user.html', name=name)


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


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
