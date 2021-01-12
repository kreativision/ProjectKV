# Home Module - Default
# Imported into the main app.py - app.register_blueprint(home_bp, url_prefix="/home")
from flask import Blueprint
from flask.templating import render_template

home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='assets',
    static_url_path='/assets'
)

@home_bp.route('/')
def home():
    return render_template('home.layout.html', title='Home')