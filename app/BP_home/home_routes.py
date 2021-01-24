from flask.templating import render_template
from app.BP_home import BP_home


projects = [
    ('New Age of Professionals', 'Logo Design', 'We had the honor of designing a brand logo for New Age of Professionals, Bhopal, India.', 'BP_home.static', 'images/bg-about-2.jpg'),
    ('Fun Food & Fasion', 'Logo Design', 'Designed complete brand package logo design for a fashion and lifestyle magazine', 'BP_home.static', 'images/bg-s1-01.png'),
    ('Dream Affairs', 'Branding', 'Complete brand package for a wedding phorography studio based out of Bhopal India', 'BP_home.static', 'images/portrait.png'),
    ('Fun Food & Fashion', 'Poster Design', 'Posters for print and media coverage designed for Fun Food and Fashion Magazine.', 'BP_home.static', 'images/bg-about-2.jpg')
]

@BP_home.route('/')
def home():
    return render_template('home.html', title='Home', projects=projects)