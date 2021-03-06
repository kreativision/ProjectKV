# This file contains the database ORM models to use with database.
from app import db, logger, app, ma
from flask_login import UserMixin

# To generating secure token used for password reset
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime

# Flask-Login User Manager
@logger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(10), default=None)
    dp_file = db.Column(db.String(20), nullable=False, default="default.png")
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Boolean(), default=False)
    verified = db.Column(db.Boolean(), default=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    reviews = db.relationship("Review", backref="by_user", lazy=True, uselist=True)

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
    variations = db.relationship(
        "Service", backref="catalogue", lazy=True, uselist=True
    )
    project_img = db.relationship(
        "ProjectImage", backref="for_catalogue", lazy=True, uselist=True
    )
    reviews = db.relationship("Review", backref="review_for", lazy=True, uselist=True)

    def __repr__(self):
        return f"Service Category => {self.name}, Starting @ {self.start_price}"


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(160))
    price = db.Column(db.Integer, nullable=False)
    header_img = db.Column(db.String(50), nullable=False)
    catalogue_id = db.Column(db.String(16), db.ForeignKey("catalogue.id"))
    allow_multiple = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f"Service => {self.name} is priced at {self.price}"


class ProjectImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.String(120), nullable=False)
    image_title = db.Column(db.String(80))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    catalogue_name = db.Column(
        db.Integer, db.ForeignKey("catalogue.name"), nullable=False
    )


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(25), db.ForeignKey("user.username"))
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text)
    catalogue = db.Column(
        db.String(25), db.ForeignKey("catalogue.name"), nullable=False
    )
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(10), default="NEW")

    def __repr__(self):
        return f"Review => {self.title} by {self.author} for catalog {self.catalogue} on {self.date}"


class Location(db.Model):
    city = db.Column(db.String(30), primary_key=True)
    map_link = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Currenly providing photography in: {self.city}"



# Schemas
class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        include_fk = True


class CatalogueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Catalogue
        include_relationships = True