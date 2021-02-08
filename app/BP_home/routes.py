from app.BP_home import BP_home
from app.BP_home.home_constants import HomeConstants, ServicesConstants
from app.models import Catalogue, Service
from flask.templating import render_template

# Temporary variables
projects = [
    (
        "New Age of Professionals",
        "Logo Design",
        "We had the honor of designing a brand logo for New Age of Professionals, Bhopal, India.",
        "BP_home.static",
        "images/bg-about-2.jpg",
    ),
    (
        "Fun Food & Fasion",
        "Logo Design",
        "Designed complete brand package logo design for a fashion and lifestyle magazine",
        "BP_home.static",
        "images/welcome-art.png",
    ),
    (
        "Dream Affairs",
        "Branding",
        "Complete brand package for a wedding phorography studio based out of Bhopal India",
        "BP_home.static",
        "images/portrait.png",
    ),
    (
        "Fun Food & Fashion",
        "Poster Design",
        "Posters for print and media coverage designed for Fun Food and Fashion Magazine.",
        "BP_home.static",
        "images/bg-about-2.jpg",
    ),
]

reviews = [
    (
        "Its like subway",
        "Jane Doe",
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys",
        "Poster Design",
        "January 24, 2020",
    ),
    (
        "They make it so easy",
        "Someone out there",
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Repellendus libero endis temporibus reicinostrum eaque, est ad dolor consequuntur, sunt aliquam quasi veniam. Vero deserunt inventore unde, accusantium dolor enim facilis? Vero deserunt inventore unde, accusantium dolor enim facilis?",
        "Logo Design",
        "June 30, 2020",
    ),
    (
        "Reaching audience, simplefied",
        "Dr. Reenu Yadav",
        "",
        "Brochures",
        "September 01, 2020",
    ),
    (
        "Easy Peasy",
        "Jane Doe",
        "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC",
        "PDF Edit",
        "October 12, 2020",
    ),
    (
        "Right Colors for right occassion",
        "Jane Doe",
        '"Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32',
        "Poster Design",
        "November 18, 2020",
    ),
    (
        "Sound Advice.",
        "RD Barman",
        "Why do we use it? It is a long established fact that a reader will be distracted by the readable",
        "Consultation",
        "January 26, 2021",
    ),
    (
        "Sound Advice.",
        "RD Barman",
        '"But I must explain to you how all this mistaken idea of denouncing pleasure',
        "Other  Stuff",
        "January 13, 2021",
    ),
]


@BP_home.route("/")
def home():
    catalogue = Catalogue.query.order_by(Catalogue.start_price).all()
    return render_template(
        "home.html",
        title="Home",
        projects=projects,
        services=catalogue,
        reviews=reviews,
        labels=HomeConstants.labels,
    )


@BP_home.route("/services")
def service_list():
    catalogue = Catalogue.query.all()
    return render_template(
        "services.html",
        title="Services",
        catalogue=catalogue,
        labels=ServicesConstants.labels,
    )
