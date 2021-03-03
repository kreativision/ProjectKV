# This is the global app routes file.
import os
from flask.helpers import send_from_directory
from app import app
from app.models import User, Review
from flask.json import jsonify

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
        return jsonify({"registered": 1})
    else:
        return jsonify({"registered": 0})


@app.route("/api/fetch-user/<string:email>", methods=["GET"])
def fetch_user(email):
    user = User.query.filter_by(email=email).first()
    return jsonify(
        {"contact": user.contact, "username": user.username, "email": user.email}
    )

# DYNAMIC API TO FETCH A REVIEW DATA - ADDED 0303
@app.route("/api/review-data/<int:id>", methods=['GET'])
def fetch_review(id):
    review = Review.query.filter_by(id=id).first()
    return jsonify({"title":review.title, "content":review.content})