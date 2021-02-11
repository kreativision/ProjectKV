from flask import Blueprint

BP_account = Blueprint(
    "BP_account",
    __name__,
    template_folder="templates",
    static_folder="assets",
    static_url_path="/BP_account/assets",
)