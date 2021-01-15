# This is the main application file.
# All the configurations for the entire application goes here.
from flask import Flask, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# Blueprints.
from app.BP_home import BP_home
from app.BP_auth import BP_auth

# App config.
app = Flask(__name__)
app.config['SECRET_KEY'] = '72a11398ef34db96b2cc7293218cbf49'
# Database config.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/databse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
encryptor = Bcrypt(app)

app.register_blueprint(BP_home, url_prefix="/home")
app.register_blueprint(BP_auth, url_prefix="/auth")
# Services Blueprint is not connected here at the time.

# Routes are imported after the configuration to avoid 'circular-import' errors.
from app import routes


# C:\Users\Amittras\Desktop\trying clone\ProjectKV\app\database