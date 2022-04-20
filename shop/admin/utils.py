from shop import db
from shop.models import User


class UserInfo:
    def __init__(self):
        self.register = db.session.query(User).count()
        self.activate = User.query.filter(User.active == 'True').count()
        self.activate = User.query.filter(User.active == 'False').count()

