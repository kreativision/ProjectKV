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
from app.models import User, Catalogue, Service, Project, ProjectImage


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
        image="wordgrams.png",
    )
    logo_2 = Service(
        name="Monogram Logo",
        description="Monogramss or lettermarks are logos that consist of letters, usually brand initials. Think about IBM, HBO...Acronyms or a company’s initials",
        price=999,
        catalogue=logos,
        image="monograms.png",
    )
    logo_3 = Service(
        name="Symbol Logo",
        description="A pictorial mark (sometimes called brand mark or logo symbol) is an icon—or graphic-based logo. For Example, the logo of Apple",
        price=1399,
        catalogue=logos,
        image="symbols.png",
    )
    poster_1 = Service(
        name="Web Posters",
        description="Optimized for fast web transfer and good quality viewing on all kinds of screens, these are best for social media campaigns.",
        price=349,
        catalogue=posters,
        image="web-poster.png",
    )
    poster_2 = Service(
        name="Print Media",
        description="Focused on the picture quality, use our print media designs which are specifically optimized for high quality printing.",
        price=449,
        catalogue=posters,
        image="print-media.png",
    )
    vCard_1 = Service(
        name="One Sided",
        description="A basic card, with the most important contact information on one side with a blank side for last minute additions by hand for extra flair.",
        price=249,
        catalogue=vCards,
        image="vCardSS.jpg",
    )
    vCard_2 = Service(
        name="Double Sided",
        description="For those who have more to tell, our double sided vCard design makes sure to utilize all the space available for a proper introduction to your clients",
        price=349,
        catalogue=vCards,
        image="vCardDS.jpg",
    )
    # addind all services to session and commit
    db.session.add_all([logo_1, logo_2, logo_3, poster_1, poster_2, vCard_1, vCard_2])
    db.session.commit()
    print("====> Adding Projects")
    project1 = Project(
        name="Test Project 1",
        service="Logo Design",
        description="This is Project 1. Ducimus accusantium dignissimos quod ipsum illo nisi deserunt accusamus nihil, quisquam sunt. Lorem, ipsum dolor sit amet consectetur adipisicing elit. Ducimus accusantium dignissimos quod ipsum illo nisi deserunt accusamus nihil, quisquam sunt.",
    )
    project2 = Project(
        name="Project Number 2",
        service="Branding Package",
        description="This is Branding Project No. 2. Ducimus accusantium dignissimos quod ipsum illo nisi deserunt accusamus nihil, quisquam sunt. Lorem, ipsum dolor sit amet consectetur adipisicing elit. Ducimus accusantium dignissimos quod ipsum illo nisi deserunt accusamus nihil, quisquam sunt.",
    )
    image1 = ProjectImage(filepath="random-1.jpg", owner_project=project1)
    image2 = ProjectImage(filepath="random-2.jpg", owner_project=project1)
    image3 = ProjectImage(filepath="random-3.jpg", owner_project=project1)
    image4 = ProjectImage(filepath="random-4.jpg", owner_project=project1)
    image5 = ProjectImage(filepath="random-5.jpg", owner_project=project1)
    image6 = ProjectImage(filepath="random-6.jpg", owner_project=project1)
    image7 = ProjectImage(filepath="random-7.jpg", owner_project=project2)
    image8 = ProjectImage(filepath="random-8.jpg", owner_project=project2)
    image9 = ProjectImage(filepath="random-9.jpg", owner_project=project2)
    image10 = ProjectImage(filepath="random-10.jpg", owner_project=project2)
    image11 = ProjectImage(filepath="random-11.jpg", owner_project=project2)
    image12 = ProjectImage(filepath="random-12.jpg", owner_project=project2)
    # adding projects and project images to session and commit
    db.session.add_all([project1, project2])
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