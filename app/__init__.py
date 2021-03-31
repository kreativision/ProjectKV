# This is the main application file.
# All the configurations for the entire application goes here.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
import os

# Blueprints.
from app.BP_home import BP_home
from app.BP_auth import BP_auth
from app.BP_account import BP_account
from app.BP_admin import BP_admin

# App config.
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_APP_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("FLASK_DB_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("FLASK_MAIL_ID")
app.config["MAIL_PASSWORD"] = os.environ.get("FLASK_MAIL_PWD")
mail = Mail(app)

encryptor = Bcrypt(app)
logger = LoginManager(app)
logger.login_view = "BP_auth.login"
logger.login_message_category = "info"
logger.login_message = ["Please login", "You need to login to view this page"]

# Routes are imported after the configuration to avoid 'circular-import' errors.
from app import routes
from app.BP_home import routes
from app.BP_auth import routes
from app.BP_account import routes
from app.BP_admin import routes

# Blueprint registration
app.register_blueprint(BP_home)
app.register_blueprint(BP_auth)
app.register_blueprint(BP_account)
app.register_blueprint(BP_admin)




# setting up cli command to bootstrap the database with mock data for development
import click
from flask.cli import with_appcontext
from app.models import User, Catalogue, Service, ProjectImage, Review, Location


@click.command(name="create")
@with_appcontext
def create():
    # reset database
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
        description="Visiting cards are more than just your contact. It is also the first exposure to the overall image of your business.",
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
        header_img="logo-wg.png",
    )
    logo_2 = Service(
        name="Monogram Logo",
        description="Monogramss or lettermarks are logos that consist of letters, usually brand initials. Think about IBM, HBO...Acronyms or a company’s initials",
        price=999,
        catalogue=logos,
        header_img="logo-mg.png",
    )
    logo_3 = Service(
        name="Symbol Logo",
        description="A pictorial mark (sometimes called brand mark or logo symbol) is an icon—or graphic-based logo. For Example, the logo of Apple",
        price=1399,
        catalogue=logos,
        header_img="logo-sym.png",
    )
    poster_1 = Service(
        name="Web Posters",
        description="Optimized for fast web transfer and good quality viewing on all kinds of screens, these are best for social media campaigns.",
        price=349,
        catalogue=posters,
        header_img="poster-web.png",
        allow_multiple=True
    )
    poster_2 = Service(
        name="Print Media",
        description="Focused on the picture quality, use our print media designs which are specifically optimized for high quality printing.",
        price=449,
        catalogue=posters,
        header_img="poster-prt.png",
        allow_multiple=True
    )
    vCard_1 = Service(
        name="One Sided vCard",
        description="A basic card, with the most important contact information on one side with a blank side for last minute additions by hand for extra flair.",
        price=249,
        catalogue=vCards,
        header_img="vcard-ss.png",
    )
    vCard_2 = Service(
        name="Double Sided vCard",
        description="For those who have more to tell, our double sided vCard design makes sure to utilize all the space available for a proper introduction to your clients",
        price=349,
        catalogue=vCards,
        header_img="vcard-ds.png",
    )
    db.session.add_all([logo_1, logo_2, logo_3, poster_1, poster_2, vCard_1, vCard_2])
    db.session.commit()

    print("====> Adding user reviews")
    # Adding reviews
    review1 = Review(by_user=tester, title="Always good stuff", review_for=logos)
    review2 = Review(
        by_user=tester,
        title="It gets better every time.",
        content="It seems like every time I make an order, the design quality gets better. These people always keep learning.",
        review_for=posters,
    )
    review3 = Review(
        by_user=tester1, title="Consultations are great", review_for=vCards
    )
    review4 = Review(
        by_user=tester1,
        title="Print quality is uncompromised",
        content="The designs print just as what looks on the screen, clean, high-quality and vibrant.",
        review_for=vCards,
    )
    review5 = Review(
        by_user=tester1,
        title="Timely Work",
        content="No matter how urgent you need something done, they're ready to get it done for you. Pretty Neat!!",
        review_for=vCards,
    )
    db.session.add_all([review1, review2, review3, review4, review5])
    db.session.commit()

    print("====> Adding Showcase Images")
    # showcase blog images
    image1 = ProjectImage(
        filepath="random-1.jpg",
        for_catalogue=logos,
        image_title="Description for img 1",
    )
    image2 = ProjectImage(
        filepath="random-2.jpg",
        for_catalogue=logos,
        image_title="Description for img 2",
    )
    image3 = ProjectImage(
        filepath="random-3.jpg",
        for_catalogue=logos,
        image_title="Description for img 3",
    )
    image4 = ProjectImage(
        filepath="random-4.jpg",
        for_catalogue=logos,
        image_title="Description random text",
    )
    image5 = ProjectImage(
        filepath="random-5.jpg",
        for_catalogue=posters,
        image_title="Poster description 001",
    )
    image6 = ProjectImage(
        filepath="random-6.jpg",
        for_catalogue=posters,
        image_title="Poster description 002",
    )
    image7 = ProjectImage(
        filepath="random-7.jpg",
        for_catalogue=posters,
        image_title="Poster description third",
    )
    image8 = ProjectImage(
        filepath="random-8.jpg",
        for_catalogue=posters,
        image_title="Poster description some ther",
    )
    image9 = ProjectImage(
        filepath="random-9.jpg",
        for_catalogue=posters,
        image_title="Poster description gone now",
    )
    image10 = ProjectImage(
        filepath="random-10.jpg",
        for_catalogue=vCards,
        image_title="vCard Description here",
    )
    image11 = ProjectImage(
        filepath="random-11.jpg",
        for_catalogue=vCards,
        image_title="vCard Description here",
    )
    image12 = ProjectImage(
        filepath="random-12.jpg",
        for_catalogue=vCards,
        image_title="vCard Description here",
    )
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

    print("====> Adding Active HQ Location")
    # adding HQ location for home page.
    location = Location(
        city="Satna, Madhya Pyadesh",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d116104.96624209618!2d80.73300773507893!3d24.579524519366984!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39847f12a0d55141%3A0xa6208334386e35e2!2sSatna%2C%20Madhya%20Pradesh!5e0!3m2!1sen!2sin!4v1616394816807!5m2!1sen!2sin",
    )
    db.session.add(location)
    db.session.commit()

    print("====> Database created with mock-data")

# Adding command to cli library
app.cli.add_command(create)