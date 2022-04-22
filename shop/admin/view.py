from flask import render_template, url_for, redirect
from . import admin
from .utils import UserInfo
from shop.decorators import role_required, admin_required
from flask_login import login_required
from shop.models import User


@admin.route('/main')
@login_required
@admin_required
def main():
    user_info = UserInfo()
    return render_template('admin/adm_index.html', user_info=user_info)


@admin.route('/users_editor', methods=['GET', 'POST'])
@login_required
@admin_required
def users_editor():
    users = User.query.all()
    return render_template('admin/adm_users_editor.html', users=users)
