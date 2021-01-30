# This is the global app routes file.
import os
from flask import redirect, url_for, send_from_directory
from app import app, db, encryptor
from app.models import User
from app.BP_auth.forms import LoginForm, RegistrationForm
from markupsafe import Markup
from flask.helpers import flash
from flask.templating import render_template
from flask_login import login_user, logout_user, current_user

# Temporary variables
projects = [
    ('New Age of Professionals', 'Logo Design', 'We had the honor of designing a brand logo for New Age of Professionals, Bhopal, India.', 'BP_home.static', 'images/bg-about-2.jpg'),
    ('Fun Food & Fasion', 'Logo Design', 'Designed complete brand package logo design for a fashion and lifestyle magazine', 'BP_home.static', 'images/welcome-art.png'),
    ('Dream Affairs', 'Branding', 'Complete brand package for a wedding phorography studio based out of Bhopal India', 'BP_home.static', 'images/portrait.png'),
    ('Fun Food & Fashion', 'Poster Design', 'Posters for print and media coverage designed for Fun Food and Fashion Magazine.', 'BP_home.static', 'images/bg-about-2.jpg')
]

reviews = [
    ('Its like subway', 'Jane Doe', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys', 'Poster Design', 'January 24, 2020'),
    ('They make it so easy', 'Someone out there', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Repellendus libero endis temporibus reicinostrum eaque, est ad dolor consequuntur, sunt aliquam quasi veniam. Vero deserunt inventore unde, accusantium dolor enim facilis? Vero deserunt inventore unde, accusantium dolor enim facilis?', 'Logo Design', 'June 30, 2020'),
    ('Reaching audience, simplefied', 'Dr. Reenu Yadav', '', 'Brochures', 'September 01, 2020'),
    ('Easy Peasy', 'Jane Doe', 'Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC', 'PDF Edit', 'October 12, 2020'),
    ('Right Colors for right occassion', 'Jane Doe', '"Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32', 'Poster Design', 'November 18, 2020'),
    ('Sound Advice.', 'RD Barman', 'Why do we use it? It is a long established fact that a reader will be distracted by the readable', 'Consultation', 'January 26, 2021'),
    ('Sound Advice.', 'RD Barman', '"But I must explain to you how all this mistaken idea of denouncing pleasure', 'Other  Stuff', 'January 13, 2021')
]

services = [
    ('1', 'Poster Designing', 'Present your audience with the right information, in the right way with our modern, catchy poster designs', '349'),
    ('2', 'Logo Designing', 'Give your business the identity it needs, choose from our variety of logo design styles and choose the one that reflects your style', '699'),
    ('1', 'Brochures Designing', 'Let your audience know exactly what you do, just at a glance with the right pick-and-read tool or just a little get-know-us card', '399'),
]


# The App Icon for browsers.
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'images/favicon.ico', mimetype='image/vnd.microsoft.icon')

# Redirect to the home-page by default.
@app.route("/")
def index():
    return render_template('home.html', title='Home', projects=projects, services=services, reviews=reviews)

@app.route('/services')
def service_list():
    return render_template('services.html', title='Services')

# Registration page
@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        content = [f'Session Active', f'You are already logged in.']
        flash(content, category='info')
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user_name = form.username.data.title()
        user_password = encryptor.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=user_name, email=form.email.data, password=user_password, contact=form.contact.data)
        db.session.add(new_user)
        db.session.commit()
        content = [f'Account Created!', Markup(f'Welcome {user_name}.<br>Please login using your <strong>email</strong> and <strong>password</strong>.')]
        flash(content, category='success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Create Account", page="Register", form=form)

# Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        content = [f'Session Active', f'You are already logged in.']
        flash(content, category='info')
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and encryptor.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            content = [f'Login Successful', f'You have been successfully logged in.']
            flash(content, category='success')
            return redirect(url_for('index'))
        else:
            content = [f'Login Failed.', Markup(f'<strong>Incorrect credentials</strong>.<br>Please try again!')]
            flash(content, category='danger')
    return render_template("login.html", title="Login", page="Login. . .", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


# Password Recovery
@app.route("/forgot-password")
def recovery():
    content = [f'Coming Soon', f'This feature is not yet available.']
    flash(content, category='info')
    return render_template('pwd-recovery.html', title="Account Recovery", page="Recover Account")

