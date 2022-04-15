from flask import render_template
from shop import rbac
from .utils import UserInfo
from flask_login import login_required
from . import admin

#
# @admin.route('/main')
# @rbac.allow(roles=['Администратор'], methods=['GET', 'POST'], endpoint='admin.index')
# @login_required
# def main():
#     user_info = UserInfo()
#     return render_template('admin/adm_index.html', user_info=user_info)
