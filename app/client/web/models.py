from web import db
from web import login
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    token = db.Column(db.String(1024))
    tokenLeaseStart = db.Column(db.DateTime)
    authenticated = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return "<Local User {}>".format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
