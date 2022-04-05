import datetime
import uuid

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from flask_security import SQLAlchemyUserDatastore
from flask_security.models import fsqla_v2 as fsqla
import shop

fsqla.FsModels.set_db_info(shop.db)


class RolesUsers(shop.db.Model):
    __tablename__ = 'roles_users'
    __table_args__ = {'extend_existing': True}
    user_id = shop.db.Column('user_id', UUID(as_uuid=True), shop.db.ForeignKey('users.id'), primary_key=True)
    role_id = shop.db.Column('role_id', UUID(as_uuid=True), shop.db.ForeignKey('roles.id'), primary_key=True)


class User(shop.db.Model, fsqla.FsUserMixin):
    __tablename__ = 'users'
    id = shop.db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = shop.db.Column(shop.db.String, unique=False)
    username = shop.db.Column(shop.db.String(64), nullable=False)
    surname = shop.db.Column(shop.db.String(64), nullable=True)
    password = shop.db.Column(shop.db.String(255), nullable=False)
    active = shop.db.Column(shop.db.Boolean(), nullable=False, default=False)
    fs_uniquifier = shop.db.Column(shop.db.String(64))
    confirmed_at = shop.db.Column(shop.db.DateTime())
    last_login_at = shop.db.Column(shop.db.DateTime())
    current_login_at = shop.db.Column(shop.db.DateTime())
    last_login_ip = shop.db.Column(shop.db.String(64))
    current_login_ip = shop.db.Column(shop.db.String(64))
    login_count = shop.db.Column(shop.db.Integer)
    tf_primary_method = shop.db.Column(shop.db.String(64), nullable=True)
    tf_totp_secret = shop.db.Column(shop.db.String(255), nullable=True)
    tf_phone_number = shop.db.Column(shop.db.String(128), nullable=True)
    create_datetime = shop.db.Column(shop.db.DateTime, nullable=False, server_default=func.now())
    update_datetime = shop.db.Column(shop.db.DateTime(), nullable=False, server_default=func.now(),
                                     onupdate=datetime.datetime.utcnow)
    us_totp_secrets = shop.db.Column(shop.db.Text, nullable=True)
    us_phone_number = shop.db.Column(shop.db.String(128), nullable=True)




class Role(shop.db.Model, fsqla.FsRoleMixin):
    __tablename__ = 'roles'
    id = shop.db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = shop.db.Column(shop.db.String, unique=True)
    description = shop.db.Column(shop.db.String(255))
    permissions = shop.db.Column(shop.db.String(255))
    update_datetime = shop.db.Column(shop.db.DateTime(), nullable=False, server_default=func.now(),
                                     onupdate=datetime.datetime.utcnow())


user_datastore = SQLAlchemyUserDatastore(shop.db, User, Role)
