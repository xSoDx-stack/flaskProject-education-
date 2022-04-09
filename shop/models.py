import uuid
from os import getenv
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous.exc import BadData
# import jwt
import shop

user_role = shop.db.Table('user_role',
                          shop.db.Column('user_id', UUID(as_uuid=True), shop.db.ForeignKey('users.id')),
                          shop.db.Column('role_id', UUID(as_uuid=True), shop.db.ForeignKey('roles.id'))
                          )


class User(shop.db.Model):
    __tablename__ = 'users'
    id = shop.db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = shop.db.Column(shop.db.String, unique=False)
    name = shop.db.Column(shop.db.String(64), nullable=False)
    surname = shop.db.Column(shop.db.String(64), nullable=True)
    password_hash = shop.db.Column(shop.db.Text())
    illegal_login_attempts = shop.db.Column(shop.db.Integer, nullable=True)
    account_status = shop.db.Column(shop.db.String(64), nullable=True)
    role = shop.db.relationship('Role', secondary=user_role, back_populates='user')

    @property
    def password(self):
        raise AttributeError('Запрещенн доступ к паролю')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_validation(self, password):
        return check_password_hash(self.password_hash, password)

    # def get_generated_token(self, expires_in=600):
    #     return jwt.encode({'reset_password': str(self.id), 'exp': time() + expires_in}, getenv('SECRET_KEY'),
    #                       algorithm='HS256').encode('utf-8')
    def get_generated_token(self):
        return shop.serialize.dumps(
            {'id': str(self.id), 'email': self.email, 'name': self.name, 'account_status': 'Active'}).encode('utf-8')

    @staticmethod
    def verify_token(token):
        try:
            # data = jwt.decode(token, getenv('SECRET_KEY'),
            #                   algorithms=['HS256'])['reset_password']
            data = shop.serialize.loads(token, max_age=6000)
        except BadData:
            return
        print(data)
        return data

    @staticmethod
    def role_insert(user):
        if user.email == getenv('MAIL_USERNAME'):
            shop.db.session.add(user)
            role = Role(name='Администратор')
            shop.db.session.add(role)
            role.user.append(user)
            shop.db.session.commit()
        else:
            shop.db.session.add(user)
            shop.db.session.commit()


class Role(shop.db.Model):
    __tablename__ = 'roles'
    id = shop.db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = shop.db.Column(shop.db.String, unique=True)
    user = shop.db.relationship('User', secondary=user_role, back_populates='role')
