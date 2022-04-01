from flask import redirect, session, url_for, render_template

from shop import app


@app.route('/')
def index():
    if session.get('user_id'):
        redirect(url_for('auth.my'))

    return render_template('index.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
