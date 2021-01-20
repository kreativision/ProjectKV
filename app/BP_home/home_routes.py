from flask.templating import render_template
from app.BP_home import BP_home

@BP_home.route('/')
def home():
    return render_template('home.html', title='Home')