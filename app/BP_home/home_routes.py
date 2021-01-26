from flask.templating import render_template
from app.BP_home import BP_home


projects = [
    ('New Age of Professionals', 'Logo Design', 'We had the honor of designing a brand logo for New Age of Professionals, Bhopal, India.', 'BP_home.static', 'images/bg-about-2.jpg'),
    ('Fun Food & Fasion', 'Logo Design', 'Designed complete brand package logo design for a fashion and lifestyle magazine', 'BP_home.static', 'images/bg-s1-01.png'),
    ('Dream Affairs', 'Branding', 'Complete brand package for a wedding phorography studio based out of Bhopal India', 'BP_home.static', 'images/portrait.png'),
    ('Fun Food & Fashion', 'Poster Design', 'Posters for print and media coverage designed for Fun Food and Fashion Magazine.', 'BP_home.static', 'images/bg-about-2.jpg')
]

reviews = [
    ('Its like subway', 'Jane Doe', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys', 'Poster Design', 'January 24, 2020'),
    ('They make it so easy', 'Someone out there', 'standard dummy text ever since the 1500s, when an unknown printer', 'Logo Design', 'June 30, 2020'),
    ('Branding Simplified', 'Dr. Reenu Yadav', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Repellendus libero endis temporibus reicinostrum eaque, est ad dolor consequuntur, sunt aliquam quasi veniam. Vero deserunt inventore unde, accusantium dolor enim facilis? Vero deserunt inventore unde, accusantium dolor enim facilis?', 'Brochures', 'September 01, 2020'),
    ('Easy Peasy', 'Jane Doe', 'Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC', 'PDF Edit', 'October 12, 2020'),
    ('Right Colors for right occassion', 'Jane Doe', '"Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32', 'Poster Design', 'November 18, 2020'),
    ('Sound Advice.', 'RD Barman', 'Why do we use it? It is a long established fact that a reader will be distracted by the readable', 'Consultation', 'January 26, 2021'),
    ('Sound Advice.', 'RD Barman', '"But I must explain to you how all this mistaken idea of denouncing pleasure', 'Other  Stuff', 'January 13, 2021')
]

@BP_home.route('/')
def home():
    return render_template('home.html', title='Home', projects=projects, reviews=reviews)