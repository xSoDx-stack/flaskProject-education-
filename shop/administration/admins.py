from flask import session, redirect, url_for, render_template
from . import admin
from .adm_class import UserInfo


@admin.route('/admin')
def admin():
    if session.get('role') == "Администратор":
        user_info = UserInfo()
    else:
        return redirect(url_for('auth.my'))
    return render_template('admin/adm_index.html', user_info=user_info)
