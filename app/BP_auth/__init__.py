# This is the main configuration file for the
# Home Blueprint

from flask import Blueprint

BP_auth = Blueprint(
    'BP_auth', __name__,
    template_folder='templates',
    static_folder='assets',
    static_url_path='/assets'
)

# Routes are imported after the configuration to avoid 'circular-import' errors.
from app.BP_auth import auth_routes