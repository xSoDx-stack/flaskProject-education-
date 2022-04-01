from flask import session, redirect, url_for, render_template
from . import admin
from shop import db
from shop.models import User


@admin.route('/admin')
def admin():
    if session.get('user_id') and session.get('role'):
        if session.get('role') == 'Администратор':
            class UserInfo:
                register = db.session.query(User).count()
                activate = User.query.filter(User.account_status == 'Active').count()
                inactivate = User.query.filter(User.account_status == 'Inactive').count()
                block = User.query.filter(User.account_status == 'Block').count()
            return render_template('admin/index.html', user_info=UserInfo)
        else:
            return redirect(url_for('auth.my'))
    return redirect(url_for('auth.login'))


