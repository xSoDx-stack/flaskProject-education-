from flask import render_template, url_for, redirect, session, request

from shop import db
from shop.auth.form import LogIn, Registr, RequestResetPassword, ResetPassword
from shop.models import User
from . import auth
from .email import send_password_reset_email, user_activate_account


@auth.route('/register', methods=['GET', 'POST'])
def register():
    _register = Registr(request.form)
    if request.method == 'POST' and _register.validate_on_submit():
        user = User.query.filter_by(email=_register.email.data).first()
        if not user:
            user = User(email=_register.email.data, name=_register.name.data, surname=_register.surname.data,
                        password=_register.password2.data, illegal_login_attempts=0, account_status='Inactive')
            User.role_insert(user)
            user_activate_account(user)
            return render_template('auth/info_message/info_activate_account.html')
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
                    if user.password_validation(_login.password.data) and user.account_status == 'Active':
                        session['user_id'] = user.id
                        session['email'] = user.email
                        session['name'] = user.name
                        if user.role:
                            session['role'] = user.role[0].name
                            return redirect(url_for('admin.admin'))
                        return redirect(url_for('auth.my'))
                    else:
                        if user.account_status != 'Inactive':
                            if user.illegal_login_attempts >= 3:
                                user.account_status = 'Block'
                                _login.email.errors = ['Аккаунт заблокирован, пройдите продцедуру востановления пароля']
                            else:
                                user.illegal_login_attempts += 1
                                db.session.add(user)
                                db.session.commit()
                                _login.email.errors = ['Неверно введена почта или пароль']
                        else:
                            user_activate_account(user)
                            _login.email.errors = ['Аккаунт не активирован на почту были отправленны инструкции']
                else:
                    _login.email.errors = ['Неверно введена почта или пароль']
            else:
                _login.email.errors = ['Неверно заполнена форма']
        return render_template('auth/login.html', login=_login)


@auth.route('/login/<token>', methods=['GET', 'POST'])
def activate_account_user(token):
    user = User.verify_token(token)
    if user:
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('auth.register'))


@auth.route('/main/my')
def my():
    if not session.get('user_id'):
        return redirect((url_for('auth.login')))
    return render_template('auth/user.html')


@auth.route('/reset_password', methods=['GET', 'POST'])
def send_password_reset():
    res_pass = RequestResetPassword()
    if request.method == 'POST' and res_pass.validate_on_submit():
        mail = User.query.filter_by(email=res_pass.email.data).first()
        if mail:
            send_password_reset_email(mail)
            return render_template('auth/info_message/info_pass_res.html')
        else:
            res_pass.email.errors = ['Пользователя с такой почтой не найдено']
    return render_template('auth/send_password_reset.html', res_pass=res_pass)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPassword()
    if form.validate_on_submit():
        if not user.account_status == 'Inactive':
            user.password = form.password2.data
            user.illegal_login_attempts = 0
            user.account_status = 'Active'
            db.session.add(user)
            db.session.commit()
            return render_template('auth/pass_successfully_changed.html')
        else:
            form.password.errors = ['Аккаунт не был активирован']
    return render_template('auth/reset_password.html', form=form)
