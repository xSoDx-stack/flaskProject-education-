import uuid
from os import getenv
from time import time

from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

import jwt
import shop


user_role = shop.db.Table('user_role',
                          shop.db.Column('user_id', UUID(as_uuid=True), shop.db.ForeignKey('users.id'), index=True,
                                         primary_key=True),
                          shop.db.Column('role_id', UUID(as_uuid=True), shop.db.ForeignKey('roles.id'), index=True,
                                         primary_key=True),
                          )


class RoleName:
    buyer = 'BUYER'
    seller = 'SELLER'
    moderator = 'MODERATOR'
    super_moderator = 'SUPER_MODERATOR'
    administer = 'ADMINISTER'


class Role(shop.db.Model):
    __tablename__ = 'roles'
    id = shop.db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4

    )
    name = shop.db.Column(
        shop.db.String,
        unique=True,
    )

    @staticmethod
    def insert_role(email):
        if email == getenv('MAIL_USERNAME'):
            role = Role(name=RoleName.administer)
            user = User(role=Role.name)
        else:
            role = Role(name=RoleName.buyer)
            user = User(role=Role.name)

        shop.db.session.add(role)
        shop.db.session.add(user)
        shop.db.session.commit()


class User(shop.db.Model):
    __tablename__ = 'users'
    id = shop.db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    email = shop.db.Column(
        shop.db.String,
        unique=False
    )
    name = shop.db.Column(
        shop.db.String(64),
        nullable=False
    )
    surname = shop.db.Column(
        shop.db.String(64),
        nullable=True
    )
    password_hash = shop.db.Column(
        shop.db.Text()
    )
    illegal_login_attempts = shop.db.Column(
        shop.db.Integer,
        nullable=True
    )
    account_status = shop.db.Column(
        shop.db.String(64),
        nullable=True
    )
    role = shop.db.relationship('roles', secondary=user_role, lazy='subquery',
                                backref=shop.db.backref('role', lazy=True))


    @property
    def password(self):
        raise AttributeError('Запрещенн доступ к паролю')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_validation(self, password):
        return check_password_hash(self.password_hash, password)

    def get_generated_token(self, expires_in=600):
        return jwt.encode({'reset_password': str(self.id), 'exp': time() + expires_in}, getenv('SECRET_KEY'),
                          algorithm='HS256').encode('utf-8')

    @staticmethod
    def verify_token(token):
        try:
            data = jwt.decode(token, getenv('SECRET_KEY'),
                              algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(data)
