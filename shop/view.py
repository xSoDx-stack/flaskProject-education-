from flask import redirect, url_for, render_template
from flask_login import login_required, logout_user
from shop import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
