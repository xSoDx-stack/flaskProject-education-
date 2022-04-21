from flask import render_template, url_for, redirect
from . import admin
from .utils import UserInfo
from shop.decorators import role_required
from flask_login import login_required


@admin.route('/main')
@login_required
@role_required('admin')
def main():
    user_info = UserInfo()
    return render_template('admin/adm_index.html', user_info=user_info)
