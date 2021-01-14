from flask import Blueprint

BP_home = Blueprint(
    'BP_home', __name__,
    template_folder='templates',
    static_folder='assets',
    static_url_path='/assets'
)

from app.BP_home import home_routes
