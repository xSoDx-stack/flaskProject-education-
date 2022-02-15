from flask import render_template, redirect, url_for, session, request
from shop.form import LogIn, Registr
from shop import app, db
from shop.models import User


@app.route('/')
def index():
    if not session.get('is_auth'):
        return redirect('/login')
    else:
        return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_not_found(e):
    return render_template('500.html'), 500


@app.route('/user/<name>')
def user():
    user = User.query.filter(User.id == session['user_id'])
    return render_template('user.html', name=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect('/user')

    login = LogIn()

    if request.method == "POST":
        if not login.validate_on_submit():
            return render_template('login.html', login=login)

        user = User.query.filter(User.email == login.email.data).first()
        if not user or user.pasword_validation(login.password.data):
            login.email.errors.append('Неверное имя или пароль')
        else:
            session['user_id'] = user.id
            session['email'] = login.email
            return redirect('/user')
    return render_template('login.html', login=login)


@app.route('/register', methods=['GET', 'POST'])
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
    return render_template('registration.html', register=register)
