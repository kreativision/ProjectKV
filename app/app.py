from flask import Flask, redirect
from flask.templating import render_template
from BP_home.home_bp import home_bp
from BP_services.services_bp import services_bp
from BP_auth.auth_bp import auth_bp
from flask.helpers import url_for


app = Flask(__name__)
app.config['SECRET_KEY'] = '72a11398ef34db96b2cc7293218cbf49'
app.register_blueprint(home_bp, url_prefix="/home")
app.register_blueprint(services_bp, url_prefix="/services")
app.register_blueprint(auth_bp, url_prefix="/auth")


session = True

@app.route("/")
def index():
    return redirect(url_for("home_bp.home"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6174, debug=True)
    # to run the app ONLY in the default localhost:5000 or 127.0.0.1:5000, use line
    # app.run(debug=True)
