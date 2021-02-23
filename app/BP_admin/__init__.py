from flask import Blueprint

BP_admin = Blueprint(
    "BP_admin",
    __name__,
    template_folder="templates",
    static_folder="assets",
    static_url_path="/BP_admin/assets",
)