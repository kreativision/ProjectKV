# This is the global app routes file.
from flask import redirect, url_for
from app import app

# Redirect to the home-page by default.
@app.route("/")
def index():
    return redirect(url_for("BP_home.home"))