# This is the main configuration file for the
# Home Blueprint

from flask import Blueprint

BP_auth = Blueprint(
    "BP_auth",
    __name__,
    template_folder="templates",
    static_folder="assets",
    static_url_path="/BP_auth/assets",
)