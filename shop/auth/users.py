from flask import render_template, url_for, redirect, request
from flask_login import login_user, login_required, current_user
from shop import db
from shop.auth.form import LogInForm, RegistrForm, RequestResetPasswordForm, ResetPasswordForm
from shop.models import User
from . import auth
from .utils import send_password_reset_email, user_activate_account


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if not current_user.is_authenticated:
        _register = RegistrForm()
        if request.method == 'POST' and _register.validate_on_submit():
            user = User.query.filter_by(email=_register.email.data).first()
            if not user:
                user = User(email=_register.email.data, name=_register.name.data, surname=_register.surname.data,
                            password=_register.confirm_password.data, current_login_ip=request.remote_addr)
                db.session.add(user)
                db.session.commit()
                user_activate_account(user)
                return render_template('auth/info_message/info_activate_account.html')
            else:
                _register.email.errors = ['Пользователь с такой почтой уже зарегистрирован']
    else:
        return redirect(url_for('auth.my'))
    return render_template('auth/registration.html', register=_register)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        _login_form = LogInForm()
        if _login_form.validate_on_submit():
            user = User.query.filter_by(email=_login_form.email.data).first()
            if user and user.password_validation(_login_form.password.data):
                if user.active:
                    login_user(user, _login_form.remember_me.data)
                    current_user.last_ip(request.remote_addr)
                    return redirect(url_for('auth.my'))
                else:
                    _login_form.email.errors = ["Ваша учётная запись не подтверждена, "
                                                "выслано повторное письмо для подтверждения"]
                    user_activate_account(user)
            else:
                _login_form.email.errors = ["Неправильный логин или пароль"]
    else:
        return redirect(url_for('auth.my'))
    return render_template('auth/login.html', login=_login_form)


@auth.route('/confirm/<token>', methods=['GET', 'POST'])
def activate_account_user(token):
    if not current_user.is_authenticated:
        user = User.query.filter(User.fs_uniquifier == User.verify_token(token)).first()
        if user:
            login_user(user)
            user.active = True
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.my'))
    else:
        return redirect(url_for('auth.my'))
    return render_template('auth/info_message/not_valid_confirm.html')


@auth.route('/main/my')
@login_required
def my():
    if current_user.is_administrator():
        return redirect(url_for('admin.main'))
    if current_user.is_moderator():
        return redirect(url_for('admin.main'))
    if current_user.is_super_moderator():
        return redirect(url_for('admin.main'))
    if current_user.is_seller():
        return redirect(url_for('admin.main'))
    return render_template('auth/user.html')


@auth.route('/reset_password', methods=['GET', 'POST'])
def send_password_reset():
    if not current_user.is_authenticated:
        res_pass = RequestResetPasswordForm()
        if request.method == 'POST' and res_pass.validate_on_submit():
            user = User.query.filter_by(email=res_pass.email.data).first()
            if user:
                send_password_reset_email(user)
                return render_template('auth/info_message/info_pass_res.html')
            else:
                res_pass.email.errors = ['Пользователя с такой почтой не найдено']
    else:
        return redirect(url_for('auth.my'))
    return render_template('auth/send_password_reset.html', res_pass=res_pass)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_authenticated:
        form = ResetPasswordForm()
        user = User.query.filter_by(fs_uniquifier=User.verify_token(token)).first()
        if user:
            if form.validate_on_submit():
                user.password = form.confirm_password.data
                db.session.add(user)
                db.session.commit()
                return render_template('auth/pass_successfully_changed.html')
    else:
        return redirect(url_for('auth.my'))
    return render_template('auth/reset_password.html', form=form)
