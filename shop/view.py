from flask import redirect, session, url_for, render_template, current_app
from flask_security import hash_password
from shop import app
from shop.models import user_datastore
import shop


@app.route('/')
def index():
    if session.get('user_id'):
        redirect(url_for('auth.my'))

    return render_template('index.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
