# This is the main application file.
# All the configurations for the entire application goes here.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Blueprints.
from app.BP_home import BP_home
from app.BP_auth import BP_auth

# App config.
app = Flask(__name__)
app.config["SECRET_KEY"] = "72a11398ef34db96b2cc6293218cbf48"

# Database config.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/databse.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Other config
encryptor = Bcrypt(app)
logger = LoginManager(app)


# Routes are imported after the configuration to avoid 'circular-import' errors.
from app import routes
from app.BP_home import routes
from app.BP_auth import routes

# Blueprint registration
app.register_blueprint(BP_home)
app.register_blueprint(BP_auth)


# setting up cli command to bootstrap the database with mock data for development
import click
from flask.cli import with_appcontext
from app.models import User, Catalogue, Service


@click.command(name="create")
@with_appcontext
def create():
    print("====> Deleting old schema ")
    db.drop_all()
    print("====> Creating new database tables ")
    db.create_all()

    print("====> Adding Users ")
    # Adding users
    tester = User(
        username="test user",
        email="testuser@kv.com",
        contact="9876543210",
        password=encryptor.generate_password_hash("testuser").decode("utf-8"),
    )
    admin = User(
        username="admin user",
        email="admin@kv.com",
        contact="9887766554",
        password=encryptor.generate_password_hash("admin").decode("utf-8"),
        admin=True,
    )
    db.session.add(tester)
    db.session.add(admin)
    db.session.commit()

    print("====> Adding Services Catalogue ")
    # Adding Service Catalogue
    logos = Catalogue(
        id="logoOptions",
        name="Logo Design",
        description="Your logo becomes the face of your business. Did you know there are many different types of logos?",
        start_price=699,
    )
    posters = Catalogue(
        id="posterOptions",
        name="Poster Design",
        description="Whether you want to take it to the internet, or prints on a college campus, or a large banner by the highway, we do it all!",
        start_price=349,
    )
    vCards = Catalogue(
        id="vCardOptions",
        name="Visiting Cards",
        description="Visiting cards are more than just contact like title, email, website, address & phone number, it is also a first exposure to the overall image of the business.",
        start_price=249,
    )
    db.session.add(logos)
    db.session.add(posters)
    db.session.commit()

    print("====> Adding Services ")
    # Adding Services
    logo_1 = Service(
        name="Wordmark Logo",
        description="Like a lettermark, a wordmark or logotype is a font-based logo that focuses on a business’ name alone. Like Visa and Coca-Cola",
        price=699,
        catalogue=logos,
    )
    logo_2 = Service(
        name="Monogram Logo",
        description="Monogramss or lettermarks are logos that consist of letters, usually brand initials. Think about IBM, HBO...Acronyms or a company’s initials",
        price=999,
        catalogue=logos,
    )
    logo_3 = Service(
        name="Symbol Logo",
        description="A pictorial mark (sometimes called brand mark or logo symbol) is an icon—or graphic-based logo. For Example, the logo of Apple",
        price=1399,
        catalogue=logos,
    )
    db.session.add(logo_1)
    db.session.add(logo_2)
    db.session.add(logo_3)
    db.session.commit()
    poster_1 = Service(
        name="Web Posters",
        description="Optimized for fast web transfer and good quality viewing on all kinds of screens, these are best for social media campaigns.",
        price=349,
        catalogue=posters,
    )
    poster_2 = Service(
        name="Print Media",
        description="Focused on the picture quality, use our print media designs which are specifically optimized for high quality printing.",
        price=449,
        catalogue=posters,
    )
    db.session.add(poster_1)
    db.session.add(poster_2)
    db.session.commit()
    vCard_1 = Service(
        name="One Sided",
        description="A basic card, with the most important contact information on one side with a blank side for last minute additions by hand for extra flair.",
        price=249,
        catalogue=vCards,
    )
    vCard_2 = Service(
        name="Double Sided",
        description="For those who have more to tell, our double sided vCard design makes sure to utilize all the space available for a proper introduction to your clients",
        price=349,
        catalogue=vCards,
    )
    db.session.add(vCard_1)
    db.session.add(vCard_2)
    db.session.commit()
    print("====> Database created with mock-data ")


# Adding command to cli library
app.cli.add_command(create)