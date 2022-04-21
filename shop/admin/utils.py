from shop import db
from shop.models import User


class UserInfo:
    def __init__(self):
        self.register = db.session.query(User).count()
        self.activate = User.query.filter_by(active='True').count()
        self.inactivate = User.query.filter_by(active='False').count()
