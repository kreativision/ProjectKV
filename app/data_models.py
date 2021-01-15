# This file contains the database ORM models to use with database. 
from app import db

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dp_file = db.Column(db.String(20), nullable=False, default='default-dp.jpeg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f'User => {self.username} {self.email} {self.dp_file}'