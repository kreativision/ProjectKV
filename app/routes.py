# This is the global app routes file.
import os
from flask.helpers import send_from_directory
from flask import request
from app import app
from app.models import User, Review, ReviewSchema
from flask.json import jsonify
from flask_login import login_required
from app.decorators import admin_required
from app.BP_admin import BP_admin
import app.utils as utils

reviewSchema = ReviewSchema(many=True)

# The App Icon for browsers.
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "images/favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/api/check-email/<string:email>", methods=["GET"])
def check_email(email):
    is_user = User.query.filter_by(email=email).first()
    if is_user:
        return jsonify({"registered": True})
    else:
        return jsonify({"registered": False})


@app.route("/api/fetch-user/<string:email>", methods=["GET"])
@login_required
def fetch_user(email):
    user = User.query.filter_by(email=email).first()
    response = {"contact": user.contact, "username": user.username, "email": user.email}
    return jsonify(response)


@BP_admin.route("/api/review/<string:status>")
@login_required
@admin_required
def get_reviews(status):
    if status == "all":
        reviews = Review.query.order_by(Review.date.desc()).all()
    else:
        reviews = (
            Review.query.filter(Review.status == status.upper())
            .order_by(Review.date.desc())
            .all()
        )
    return jsonify(reviewSchema.dump(reviews))


@BP_admin.route("/api/review/mark-reviewed")
@login_required
@admin_required
def mark_as_read():
    utils.mark_all_as_reviewed()
    return jsonify({"success": True})


@BP_admin.route("/api/review/action", methods=["PATCH", "DELETE"])
@login_required
@admin_required
def patch_review():
    if request.method == "PATCH":
        if utils.patch_review(request.json):
            return jsonify({"success": True, "id": request.json["id"]})
        else:
            return jsonify({"success": False})
    elif request.method == "DELETE":
        utils.delete_review(request.json["id"])
        return jsonify({"success": True, "id": request.json["id"]})
