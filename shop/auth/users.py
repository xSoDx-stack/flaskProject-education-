from flask import render_template, url_for, redirect, session, request
from flask_security import hash_password, registerable
from shop import db
from shop.auth.form import LogIn, Registr, RequestResetPassword
from shop.models import user_datastore
from . import auth


@auth.route('/register', methods=['GET', 'POST'])
def register():
    _register = Registr()
    if request.method == 'POST' and _register.validate_on_submit():
        if not user_datastore.find_user(email=_register.email.data):
            registerable.register_user(_register)
            db.session.commit()
        else:
            _register.email.errors = ["Пользователь с такой почтой уже зарегестрирован"]
    return render_template('auth/registration.html', register=_register)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('auth.my'))
    else:
        _login = LogIn()
    return render_template('auth/login.html', login=_login)


@auth.route('/login/<token>', methods=['GET', 'POST'])
def activate_account_user(token):
        return redirect(url_for('auth.register'))


@auth.route('/main/my')
def my():
    if not session.get('user_id'):
        return redirect((url_for('auth.login')))
    return render_template('auth/user.html')


@auth.route('/reset_password', methods=['GET', 'POST'])
def send_password_reset():
    res_pass = RequestResetPassword()
    return render_template('auth/send_password_reset.html', res_pass=res_pass)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    return render_template('auth/reset_password.html')
