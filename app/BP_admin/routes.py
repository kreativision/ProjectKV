from app import db, encryptor
from app.BP_admin import BP_admin
from app.BP_admin.forms import EditAdminDetailsForm, EditAdminPasswordForm, EditDPForm
from app.models import User
from app.decorators import admin_required
import app.utils as utils
from flask import request, flash, redirect, url_for
from flask.templating import render_template
from flask_login import login_required, current_user


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


@BP_admin.route("/a/settings", methods=["GET", "POST"])
@login_required
@admin_required
def settings():
    edit_form_prefix = "detailsForm"
    edit_form = EditAdminDetailsForm(prefix=edit_form_prefix)
    change_pwd_form_prefix = "passwordForm"
    change_pwd_form = EditAdminPasswordForm(prefix=change_pwd_form_prefix)
    dp_form_prefix = "dpForm"
    dp_form = EditDPForm(prefix=dp_form_prefix)
    if request.method == "POST" and request.form["form"] == "pwd":
        if change_pwd_form.validate_on_submit():
            utils.change_password(change_pwd_form.new_password.data)
            content = [f"Success", f"Your assword is updated."]
            flash(content, category="success")
            return redirect(url_for("BP_admin.settings"))
    elif request.method == "POST" and request.form["form"] == "info":
        if edit_form.validate_on_submit():
            utils.update_user(edit_form.data)
            content = [f"Success", f"Your details are updated."]
            flash(content, category="success")
            return redirect(url_for("BP_admin.settings"))
    elif request.method == "POST" and request.form["form"] == "dp":
        if dp_form.validate_on_submit():
            utils.update_dp(dp_form.dp_image.data)
            content = [f"Success", f"Your profile image is updated."]
            flash(content, category="success")
            return redirect(url_for("BP_admin.settings"))
    return render_template(
        "settings.html",
        title="Admin Settings",
        detailsForm=edit_form,
        passwordForm=change_pwd_form,
        dpForm=dp_form,
    )
