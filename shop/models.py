from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from time import time
import shop
from os import getenv


class Role(shop.db.Model):
    __tablename__ = 'roles'
    id = shop.db.Column(shop.db.Integer, primary_key=True)
    name = shop.db.Column(shop.db.String, unique=True)
    users = shop.db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(shop.db.Model):
    __tablename__ = 'users'
    id = shop.db.Column(shop.db.Integer, primary_key=True)
    email = shop.db.Column(shop.db.String, unique=True)
    name = shop.db.Column(shop.db.String(64), nullable=False)
    surname = shop.db.Column(shop.db.String(64), nullable=True)
    password_hash = shop.db.Column(shop.db.Text())
    role_id = shop.db.Column(shop.db.Integer, shop.db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('Запрещенн доступ к паролю')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def pasword_validation(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, getenv('SECRET_KEY'),
                          algorithm='HS256').encode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, getenv('SECRET_KEY'),
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
