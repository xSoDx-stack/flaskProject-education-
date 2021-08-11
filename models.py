from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash,generate_password_hash


db = SQLAlchemy()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.Text)

    @property
    def password(self):
        raise AttributeError('Запрещенн доступ к паролю')


    @password.setter
    def password_hash(self, password):
        self.password_hesh = generate_password_hash(password)


    def password_valid(self, password):
      return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<User %r>' % self.email