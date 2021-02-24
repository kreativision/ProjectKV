from app.BP_admin import BP_admin
from app.models import User
from app.decorators import admin_required
from flask.templating import render_template
from flask_login import login_required

@BP_admin.route("/a/dashboard")
@login_required
@admin_required
def home():
    return render_template("index.html", title="Dashboard")


@BP_admin.route("/a/orders")
@login_required
@admin_required
def orders():
    return render_template("orders.html", title="Manage Orders")

@BP_admin.route("/a/reviews")
@login_required
@admin_required
def reviews():
    return render_template("reviews.html", title="Manage Reviews")

@BP_admin.route("/a/services")
@login_required
@admin_required
def services():
    return render_template("admin-services.html", title="Manage Services")

@BP_admin.route("/a/blog")
@login_required
@admin_required
def blog():
    return render_template("admin-blog.html", title="Manage Blog")

@BP_admin.route("/a/offers")
@login_required
@admin_required
def offers():
    return render_template("offers.html", title="Manage Offers")