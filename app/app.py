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
    # this config allows for the app to be run on the local network;
    # accessible from the phone/tablet connected to the same WiFi network as the machine on which the app is running.

    # to access the dev-server on the phone, follow these steps: 
        # open a terminal => enter command => "ipconfig"
        # look for something similar to => 'IPv4 Address. . . . . . . . . . . : 192.168.XX.XXX'
        # on your phone access the IP => 192.168.XX.XXX:6174 to view the running application.
    
    # The app would still be accessible on localhost, but with port 6174; go to 'localhost:6174'

    # to run the app ONLY in the default localhost:5000 or 127.0.0.1:5000, use line
    # 'app.run(debug=True)'

# Enable VirtualEnv
# Scripts\Activate.ps1

# Run App
# python app/app.py
