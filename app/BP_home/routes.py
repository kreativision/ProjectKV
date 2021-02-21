from app.BP_home import BP_home
from app.BP_home.home_constants import HomeConstants, ServicesConstants
from app.models import Catalogue, Service, ProjectImage
from flask.templating import render_template

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
    )
]


@BP_home.route("/")
def home():
    catalogue = Catalogue.query.order_by(Catalogue.start_price).all()
    showcase_images = ProjectImage.query.order_by(ProjectImage.date).limit(6).all()
    return render_template(
        "home.html",
        title="Home",
        showcase=showcase_images,
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


@BP_home.route("/blog")
def blog():
    return render_template("blog.html", title="Blog")

    