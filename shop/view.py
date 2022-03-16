from flask import render_template, redirect, session, url_for

from shop import app


@app.route('/')
def index():
    if session.get('user_id'):
        return redirect(url_for('auth.my'))
    else:
        return redirect(url_for('auth.login'))
