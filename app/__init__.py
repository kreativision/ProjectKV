from flask import Flask, redirect
from flask.templating import render_template
# from BP_home.home_bp import home_bp
# from BP_services.services_bp import services_bp
# from BP_auth.auth_bp import auth_bp
from app.BP_home import BP_home
from app.BP_auth import BP_auth
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '72a11398ef34db96b2cc7293218cbf49'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/databse.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(BP_home, url_prefix="/home")
app.register_blueprint(BP_auth, url_prefix="/auth")
# app.register_blueprint(services_bp, url_prefix="/services")

from app import routes