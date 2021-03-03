from app.BP_home import BP_home
from app.BP_home.home_constants import HomeConstants, ServicesConstants
from app.models import Catalogue, Service, ProjectImage, Review
from flask.templating import render_template

# @BP_home.route("/check")
# def check():
#     return render_template("test.html")

@BP_home.route("/")
def home():
    catalogue = Catalogue.query.order_by(Catalogue.start_price).all()
    showcase_images = ProjectImage.query.order_by(ProjectImage.date).limit(6).all()
    reviews = Review.query.filter(Review.status!="REMOVED").order_by(Review.date.desc()).all()
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

    