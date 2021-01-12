# Services Module
# Imported into the main app.py - app.register_blueprint(services_bp, url_prefix="/services")
from flask import Blueprint
from flask.templating import render_template

services_bp = Blueprint(
    'services_bp', __name__,
    template_folder='templates',
    static_folder='assets',
    static_url_path='/assets'
)

@services_bp.route('/')
def s_home():
    return render_template('services.layout.html', title='Services')