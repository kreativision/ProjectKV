# This is the main application file.
# All the configurations for the entire application goes here.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

# Blueprints.
from app.BP_home import BP_home
from app.BP_auth import BP_auth
from app.BP_account import BP_account

# App config.
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_APP_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("FLASK_DB_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("FLASK_MAIL_ID")
app.config["MAIL_PASSWORD"] = os.environ.get("FLASK_MAIL_PWD")
mail = Mail(app)
encryptor = Bcrypt(app)
logger = LoginManager(app)
logger.login_view = 'BP_auth.login'


# Routes are imported after the configuration to avoid 'circular-import' errors.
from app import routes
from app.BP_home import routes
from app.BP_auth import routes
from app.BP_account import routes

# Blueprint registration
app.register_blueprint(BP_home)
app.register_blueprint(BP_auth)
app.register_blueprint(BP_account)


# setting up cli command to bootstrap the database with mock data for development
import click
from flask.cli import with_appcontext
from app.models import User, Catalogue, Service, ProjectImage


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
        username="Amittras Pal",
        email="pal.amittras@gmail.com",
        contact="8871822617",
        password=encryptor.generate_password_hash("password").decode("utf-8"),
        verified=True,
    )
    admin = User(
        username="admin user",
        email="admin@kv.com",
        contact="9887766554",
        password=encryptor.generate_password_hash("admin").decode("utf-8"),
        admin=True,
        verified=True,
    )
    tester1 = User(
        username="Sukriti Shukla",
        email="sukritishukla306@gmail.com",
        contact="7352545252",
        password=encryptor.generate_password_hash("password").decode("utf-8"),
        verified=True,
    )
    db.session.add_all([tester, tester1, admin])
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
    db.session.add_all([logos, posters])
    db.session.commit()
    print("====> Adding Services ")
    # Adding Services
    logo_1 = Service(
        name="Wordmark Logo",
        description="Like a lettermark, a wordmark or logotype is a font-based logo that focuses on a business’ name alone. Like Visa and Coca-Cola",
        price=699,
        catalogue=logos,
        header_img="wordgrams.png",
    )
    logo_2 = Service(
        name="Monogram Logo",
        description="Monogramss or lettermarks are logos that consist of letters, usually brand initials. Think about IBM, HBO...Acronyms or a company’s initials",
        price=999,
        catalogue=logos,
        header_img="monograms.png",
    )
    logo_3 = Service(
        name="Symbol Logo",
        description="A pictorial mark (sometimes called brand mark or logo symbol) is an icon—or graphic-based logo. For Example, the logo of Apple",
        price=1399,
        catalogue=logos,
        header_img="symbols.png",
    )
    poster_1 = Service(
        name="Web Posters",
        description="Optimized for fast web transfer and good quality viewing on all kinds of screens, these are best for social media campaigns.",
        price=349,
        catalogue=posters,
        header_img="web-poster.png",
    )
    poster_2 = Service(
        name="Print Media",
        description="Focused on the picture quality, use our print media designs which are specifically optimized for high quality printing.",
        price=449,
        catalogue=posters,
        header_img="print-media.png",
    )
    vCard_1 = Service(
        name="One Sided",
        description="A basic card, with the most important contact information on one side with a blank side for last minute additions by hand for extra flair.",
        price=249,
        catalogue=vCards,
        header_img="vCardSS.jpg",
    )
    vCard_2 = Service(
        name="Double Sided",
        description="For those who have more to tell, our double sided vCard design makes sure to utilize all the space available for a proper introduction to your clients",
        price=349,
        catalogue=vCards,
        header_img="vCardDS.jpg",
    )
    db.session.add_all([logo_1, logo_2, logo_3, poster_1, poster_2, vCard_1, vCard_2])
    db.session.commit()
    print("====> Adding Showcase Images")
    image1 = ProjectImage(filepath="random-1.jpg", for_catalogue=logos, image_title="Description for img 1")
    image2 = ProjectImage(filepath="random-2.jpg", for_catalogue=logos, image_title="Description for img 2")
    image3 = ProjectImage(filepath="random-3.jpg", for_catalogue=logos, image_title="Description for img 3")
    image4 = ProjectImage(filepath="random-4.jpg", for_catalogue=logos, image_title="Description random text")
    image5 = ProjectImage(filepath="random-5.jpg", for_catalogue=posters, image_title="Poster description 001")
    image6 = ProjectImage(filepath="random-6.jpg", for_catalogue=posters, image_title="Poster description 002")
    image7 = ProjectImage(filepath="random-7.jpg", for_catalogue=posters, image_title="Poster description third")
    image8 = ProjectImage(filepath="random-8.jpg", for_catalogue=posters, image_title="Poster description some ther")
    image9 = ProjectImage(filepath="random-9.jpg", for_catalogue=posters, image_title="Poster description gone now")
    image10 = ProjectImage(filepath="random-10.jpg", for_catalogue=vCards, image_title="vCard Description here")
    image11 = ProjectImage(filepath="random-11.jpg", for_catalogue=vCards, image_title="vCard Description here")
    image12 = ProjectImage(filepath="random-12.jpg", for_catalogue=vCards, image_title="vCard Description here")
    db.session.add_all(
        [
            image1,
            image2,
            image3,
            image4,
            image5,
            image6,
            image7,
            image8,
            image9,
            image10,
            image11,
            image12,
        ]
    )
    db.session.commit()
    print("====> Database created with mock-data")


# Adding command to cli library
app.cli.add_command(create)