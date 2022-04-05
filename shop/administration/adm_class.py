from shop import db
from shop.models import User


class UserInfo:
    def __init__(self):
        self.register = db.session.query(User).count()
        self.activate = User.query.filter(User.account_status == 'Active').count()
        self.inactivate = User.query.filter(User.account_status == 'Inactive').count()
        self.block = User.query.filter(User.account_status == 'Block').count()
