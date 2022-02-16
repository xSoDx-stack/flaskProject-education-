from flask import render_template, redirect, session, url_for
from shop import app


@app.route('/')
def index():
    if not session.get('is_auth'):
        return redirect(url_for('auth.login'))
    else:
        return render_template('index.html')
