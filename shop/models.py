import uuid
from os import getenv
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous.exc import BadData
import shop
from sqlalchemy import func
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin


users_roles = shop.db.Table('users_roles',
                            shop.db.Column('user_id', UUID(as_uuid=True), shop.db.ForeignKey('user.id')),
                            shop.db.Column('role_id', UUID(as_uuid=True), shop.db.ForeignKey('role.id')))


class AnonymousUser(AnonymousUserMixin):
    @property
    def is_moderator(self):
        return False

    @property
    def is_administrator(self):
        return False

    @property
    def is_super_moderator(self):
        return False

    @property
    def is_seller(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return


class Role(shop.db.Model):
    id = shop.db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = shop.db.Column(shop.db.String, unique=True)
    users = shop.db.relationship('User', secondary=users_roles, back_populates='roles')

    @staticmethod
    def insert_roles():
        roles = {
            'seller',
            'moderator',
            'super_moderator',
            'admin'
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if not role:
                role = Role(name=r)
                shop.db.session.add(role)
        shop.db.session.commit()

    def __repr__(self):
        return '%r' % self.name


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
    roles = shop.db.relationship('Role', secondary=users_roles, back_populates='users')

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_validation(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def get_generated_token(self):
        return shop.serialize.dumps(self.fs_uniquifier)

    @staticmethod
    def verify_token(token):
        try:
            data = shop.serialize.loads(token, max_age=7000)
        except BadData:
            return
        return data

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.roles:
            if self.email == getenv('MAIL_USERNAME'):
                self.roles.append(Role.query.filter_by(name='admin').first())
                self.roles.append(Role.query.filter_by(name='seller').first())
                self.roles.append(Role.query.filter_by(name='moderator').first())
                self.roles.append(Role.query.filter_by(name='super_moderator').first())

    def get_id(self):
        return str(self.fs_uniquifier)

    def cant(self, role):
        answer = False
        for i in self.roles:
            if role in i.name:
                answer = role in i.name
                break
        return answer

    def is_administrator(self):
        return self.cant('admin')

    def is_super_moderator(self):
        return self.cant('super_moderator')

    def is_moderator(self):
        return self.cant('moderator')

    def is_seller(self):
        return self.cant('seller')

    def last_ip(self, ip):
        self.last_login_ip = ip
        shop.db.session.add(self)

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return "%r" % self.email


class Country(shop.db.Model):
    id = shop.db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = shop.db.Column(shop.db.String(128))

    def __repr__(self):
        return '%r' % self.name


class Type(shop.db.Model):
    id = shop.db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = shop.db.Column(shop.db.String(128))

    def __repr__(self):
        return '%r' % self.name


class Brand(shop.db.Model):
    id = shop.db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = shop.db.Column(shop.db.String(128))

    def __repr__(self):
        return '%r' % self.name


class Product(shop.db.Model):
    id = shop.db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = shop.db.Column(shop.db.String(128))
    price = shop.db.Column(shop.db.Integer())
    discription = shop.db.Column(shop.db.Text())
    manufacturer_country = shop.db.Column(UUID(), shop.db.ForeignKey('country.id'))
    type = shop.db.Column(UUID(), shop.db.ForeignKey('type.id'))
    brand = shop.db.Column(UUID(), shop.db.ForeignKey('brand.id'))
    gender = shop.db.Column(shop.db.String(64))
    material = shop.db.Column(shop.db.String(64))
    collection = shop.db.Column(shop.db.String(128))
    season = shop.db.Column(shop.db.String(64))
    colour = shop.db.Column(shop.db.String(64))
    size = shop.db.Column(shop.db.Integer())
    length = shop.db.Column(shop.db.Integer())
    height = shop.db.Column(shop.db.Integer())
    width = shop.db.Column(shop.db.Integer())
    weight = shop.db.Column(shop.db.Integer())
    update_datetime = shop.db.Column(shop.db.DateTime, nullable=False, server_default=func.now(),
                                     onupdate=datetime.utcnow)
    data_create = shop.db.Column(shop.db.DateTime, nullable=False, server_default=func.now())


shop.login_manager.anonymous_user = AnonymousUser
