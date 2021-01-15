# This file contains the database ORM models to use with database. 
from app import db, logger
from flask_login import UserMixin

@logger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dp_file = db.Column(db.String(20), nullable=False, default='default-dp.jpeg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f'User => {self.username} {self.email} {self.dp_file}'