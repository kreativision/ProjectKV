from flask import Blueprint

BP_auth = Blueprint(
    'BP_auth', __name__,
    template_folder='templates',
    static_folder='assets',
    static_url_path='/assets'
)

from app.BP_auth import auth_routes