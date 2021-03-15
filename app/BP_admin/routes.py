from app import db, encryptor
import app.utils as utils
from app.models import User, Review
from app.decorators import admin_required
from app.BP_admin import BP_admin
from app.BP_admin.forms import EditReviewForm
from app.global_forms import (
    UpdateAccountInfoForm,
    ChangeUserPasswordForm,
    UpdateDPForm,
    prefix,
)
from flask import flash, redirect, request, url_for, json
from flask.templating import render_template
from flask_login import login_required, current_user
from flask.json import jsonify


@BP_admin.route("/a/dashboard")
@login_required
@admin_required
def home():
    return render_template("dashboard.html", title="Dashboard")


@BP_admin.route("/a/order/<string:id>")
@login_required
@admin_required
def order_id(id):
    return render_template("order-details.html")


@BP_admin.route("/a/orders/<string:status>")
@login_required
@admin_required
def order_type(status):
    # orders = Order.query.filter(Order.status == status).all()
    # return render_template(
    #     "orders.html", title="Manage Orders", orders=orders, status=status
    # )
    return render_template("orders.html")


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


@BP_admin.route("/a/r/<string:type>", methods=["GET", "POST"])
@login_required
@admin_required
def review_type(type):
    edit_review_form = EditReviewForm()
    if edit_review_form.validate_on_submit():
        utils.edit_review(request.form["review_id"], edit_review_form.data)
        content = [
            "Review edited successfully!",
            "The review is moved to EDITED state.",
        ]
        flash(content, category="success")
        return redirect(request.referrer)
    if type == "all":
        reviews = Review.query.order_by(Review.date.desc()).all()
    else:
        reviews = (
            Review.query.filter(Review.status == type.upper())
            .order_by(Review.date.desc())
            .all()
        )
    return render_template(
        "reviews.html",
        title="Manage Reviews",
        reviews=reviews,
        type=type,
        editForm=edit_review_form,
    )


@BP_admin.route("/a/remove-review/<string:id>")
@login_required
@admin_required
def remove_review(id):
    utils.remove_review(id)
    content = ["Review removed successfully!", ""]
    flash(content, category="success")
    return redirect(request.referrer)


@BP_admin.route("/a/reviews/mark-as-read")
@login_required
@admin_required
def mark_all_as_reviewed():
    utils.mark_all_as_reviewed()
    content = ["Success", "All NEW reviews marked as REVIEWED."]
    flash(content, category="success")
    return redirect(url_for("BP_admin.review_type", type="new"))


@BP_admin.route("/a/delete-review/<string:revId>")
@login_required
@admin_required
def delete_review(revId):
    utils.delete_review(revId)
    content = ["Review deleted successfully.", ""]
    flash(content, category="success")
    return redirect(request.referrer)


@BP_admin.route("/a/restore-review/<string:revId>")
@login_required
@admin_required
def restore_review(revId):
    utils.restore_review(revId)
    content = ["Review restored", "The review is restored to NEW state."]
    flash(content, category="success")
    return redirect(request.referrer)


@BP_admin.route("/a/settings", methods=["GET", "POST"])
@login_required
@admin_required
def settings():
    edit_form = UpdateAccountInfoForm(prefix=prefix["info"])
    change_pwd_form = ChangeUserPasswordForm(prefix=prefix["pwd"])
    dp_form = UpdateDPForm(prefix=prefix["dp"])
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
