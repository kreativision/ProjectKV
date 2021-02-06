# This is the global app routes file.
import os
from flask.helpers import send_from_directory
from app import app

# The App Icon for browsers.
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "images/favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )
