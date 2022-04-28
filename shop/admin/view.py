from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from shop import _admin, db
from flask_login import current_user
from flask import redirect, url_for
from shop.models import Role, User, Product, Type, Country, Brand


class UserView(ModelView):
    column_list = ['email', 'name', 'surname', 'phone_number', 'active', 'roles', 'last_login_ip', 'create_datetime',
                   'update_datetime']
    form_columns = ['name', 'email', 'surname', 'phone_number', 'password', 'roles']
    column_searchable_list = ['name', 'email', 'surname', 'phone_number']
    create_modal = True
    edit_modal = True

    def is_accessible(self):
        return current_user.is_administrator

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.my'))


_admin.add_view(UserView(User, db.session))


class IndexAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_administrator

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.my'))


class RoleView(ModelView):
    def is_accessible(self):
        return current_user.is_administrator

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.my'))


_admin.add_view(RoleView(Role, db.session))


class ProductView(ModelView):
    def is_accessible(self):
        return current_user.is_administrator

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.my'))


_admin.add_view(ProductView(Product, db.session))


class CountryView(ModelView):
    can_export = True
    countries = Country()

    def is_accessible(self):
        return current_user.is_administrator

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.my'))


_admin.add_view(CountryView(Country, db.session))


class BrandView(ModelView):
    def is_accessible(self):
        return current_user.is_administrator

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.my'))


_admin.add_view(BrandView(Brand, db.session))


class TypeView(ModelView):
    def is_accessible(self):
        return current_user.is_administrator

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.my'))


_admin.add_view(TypeView(Type, db.session))


_admin.add_link(MenuLink(name="Выход", url='/logout'))
