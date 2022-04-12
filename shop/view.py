from flask import redirect, session, url_for, render_template
from flask_login import login_required, logout_user
from shop import app


@app.route('/')
def index():
    if session.get('user_id'):
        redirect(url_for('auth.my'))
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
