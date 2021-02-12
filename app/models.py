# This file contains the database ORM models to use with database.
from app import db, logger, app
from flask_login import UserMixin

# To generating secure token used for password reset
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@logger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(10), default=None)
    dp_file = db.Column(db.String(20), nullable=False, default="none.jpeg")
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Boolean(), default=False)
    verified = db.Column(db.Boolean(), default=False)

    # Generates a secure token for the user with a expiration time of 900s/15min
    def generate_token(self, expires_sec=600):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    # verifies the token provided to see if it's valid/alive
    @staticmethod  # static bcz it doesn't utilize the self parameter
    def verify_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
            return User.query.get(user_id)
        except:
            return None

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
    image = db.Column(db.String(50), nullable=False)
    catalogue_id = db.Column(db.String(16), db.ForeignKey("catalogue.id"))

    def __repr__(self):
        return f"Service => {self.name} is priced at {self.price}"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    service = db.Column(db.String(25), nullable=False)
    description = db.Column(db.Text)
    pictures = db.relationship(
        "ProjectImage", backref="owner_project", lazy=True, uselist=True
    )
    show_on_home = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return f"Service => {self.name} is priced at {self.service}"


class ProjectImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.String(120), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
