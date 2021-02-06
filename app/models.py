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
    contact = db.Column(db.String(10), default=None)
    dp_file = db.Column(db.String(20), nullable=False, default="none.jpeg")
    password = db.Column(db.String(60), nullable=False)
    # role = db.Column(db.String(10), nullable=False, default='user')
    admin = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f"User => {self.username} {self.email} {self.dp_file}"


class Catalogue(db.Model):
    id = db.Column(db.String(16), primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(160))
    start_price = db.Column(db.Integer, nullable=False)
    variations = db.relationship("Service", backref="catalogue", lazy=True)

    def __repr__(self):
        return f"Service Category => {self.name}, Starting @ {self.start_price}"


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(160))
    price = db.Column(db.Integer, nullable=False)
    catalogue_id = db.Column(db.String(16), db.ForeignKey("catalogue.id"))

    def __repr__(self):
        return f"Service => {self.name} is priced at {self.price}"
