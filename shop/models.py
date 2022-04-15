import uuid
from os import getenv
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous.exc import BadData
import shop
from sqlalchemy import func
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from flask_rbac import RoleMixin

users_roles = shop.db.Table('users_roles',
                            shop.db.Column('user_id', UUID(as_uuid=True), shop.db.ForeignKey('user.id')),
                            shop.db.Column('role_id', UUID(as_uuid=True), shop.db.ForeignKey('role.id'))
                            )

roles_parents = shop.db.Table('roles_parents',
                              shop.db.Column('role_id', UUID(as_uuid=True), shop.db.ForeignKey('role.id')),
                              shop.db.Column('parent_id', UUID(as_uuid=True), shop.db.ForeignKey('role.id'))
                              )


@shop.rbac.as_role_model
class Role(shop.db.Model, RoleMixin):
    id = shop.db.Column(UUID(as_uuid=True), primary_key=True)
    name = shop.db.Column(shop.db.String(20))
    parents = shop.db.relationship('Role', secondary=roles_parents, primaryjoin=(id == roles_parents.c.role_id),
                                   secondaryjoin=(id == roles_parents.c.parent_id),
                                   backref=shop.db.backref('children', lazy='dynamic'))

    def __init__(self, name):
        RoleMixin.__init__(self)
        self.name = name

    def add_parent(self, parent):
        self.parents.append(parent)

    def add_parents(self, *parents):
        for parent in parents:
            self.add_parent(parent)

    @staticmethod
    def get_by_name(name):
        return Role.query.filter_by(name=name).first()


@shop.rbac.as_user_model
class User(shop.db.Model, UserMixin):
    id = shop.db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = shop.db.Column(shop.db.String, unique=False)
    name = shop.db.Column(shop.db.String(64), nullable=True)
    surname = shop.db.Column(shop.db.String(64), nullable=True)
    phone_number = shop.db.Column(shop.db.String(128), nullable=True)
    fs_uniquifier = shop.db.Column(shop.db.String(128), default=uuid.uuid4, onupdate=uuid.uuid4)
    active = shop.db.Column(shop.db.Boolean(), default=False)
    password_hash = shop.db.Column(shop.db.Text())
    confirmed_at = shop.db.Column(shop.db.DateTime())
    last_login_ip = shop.db.Column(shop.db.String(64))
    current_login_ip = shop.db.Column(shop.db.String(64))
    update_datetime = shop.db.Column(shop.db.DateTime, nullable=False, server_default=func.now(),
                                     onupdate=datetime.utcnow)
    create_datetime = shop.db.Column(shop.db.DateTime, nullable=False, server_default=func.now())
    roles = shop.db.relationship('Role', secondary=users_roles, back_populates='roles')

    @property
    def password(self):
        raise AttributeError("Доступ к паролю запрещён")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_validation(self, password):
        return check_password_hash(self.password_hash, password)

    def get_generated_token(self):
        return shop.serialize.dumps(self.fs_uniquifier)

    @staticmethod
    def verify_token(token):
        try:
            data = shop.serialize.loads(token, max_age=7000)
        except BadData:
            return
        return data

    @staticmethod
    def role_insert(user):
        if user.email == getenv('MAIL_USERNAME'):
            shop.db.session.add(user)
            role = Role('administrator')
            shop.db.session.add(role)
            role.user.append(user)
            shop.db.session.commit()
        else:
            role = Role('anonymous')
            shop.db.session.add(role)
            shop.db.session.add(user)
            shop.db.session.commit()

    def get_id(self):
        return str(self.fs_uniquifier)

    def add_role(self, role):
        self.roles.append(role)

    def add_roles(self, roles):
        for role in roles:
            self.add_role(role)

    def get_roles(self):
        for role in self.roles:
            yield role
