from flask import render_template, url_for, redirect, session, request
from flask_login import login_user, login_required
from shop import db, ser_user
from shop.auth.form import LogInForm, RegistrForm, RequestResetPasswordForm, ResetPasswordForm
from shop.models import User
from . import auth
from .utils import send_password_reset_email, user_activate_account, load_user


@auth.route('/register', methods=['GET', 'POST'])
def register():
    _register = RegistrForm()
    if request.method == 'POST' and _register.validate_on_submit():
        user = User.query.filter_by(email=_register.email.data).first()
        if not user:
            user = User(email=_register.email.data, name=_register.name.data, surname=_register.surname.data,
                        password=_register.confirm_password.data, fs_uniquifier=ser_user.dumps(_register.email.data))
            User.role_insert(user)
            user_activate_account(user)
            return render_template('auth/info_message/info_activate_account.html')
        else:
            _register.email.errors = ['Пользователь с такой почтой уже зарегистрирован']
    return render_template('auth/registration.html', register=_register)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    _login_form = LogInForm()
    if _login_form.validate_on_submit():
        user = User.query.filter_by(email=_login_form.email.data).first()
        if user and user.password_validation(_login_form.password.data):
            login_user(user, _login_form.remember_me.data)
            return redirect(url_for('auth.my'))
        else:
            _login_form.email.errors = ["Неправильный логин или пароль"]
    return render_template('auth/login.html', login=_login_form)


@auth.route('/confirm/<token>', methods=['GET', 'POST'])
def activate_account_user(token):
    user = User.query.filter(User.fs_uniquifier == User.verify_token(token)).first()
    if user:
        user.active = True
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('auth/info_message/not_valid_confirm.html')


@auth.route('/main/my')
@login_required
def my():
    return render_template('auth/user.html')


@auth.route('/reset_password', methods=['GET', 'POST'])
def send_password_reset():
    res_pass = RequestResetPasswordForm()
    if request.method == 'POST' and res_pass.validate_on_submit():
        user = User.query.filter_by(email=res_pass.email.data).first()
        if user:
            send_password_reset_email(user)
            return render_template('auth/info_message/info_pass_res.html')
        else:
            res_pass.email.errors = ['Пользователя с такой почтой не найдено']
    return render_template('auth/send_password_reset.html', res_pass=res_pass)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if not user.account_status == 'Inactive':
            user.password = form.confirm_password.data
            user.illegal_login_attempts = 0
            user.account_status = 'Active'
            db.session.add(user)
            db.session.commit()
            return render_template('auth/pass_successfully_changed.html')
        else:
            form.password.errors = ['Аккаунт не был активирован']
    return render_template('auth/reset_password.html', form=form)
