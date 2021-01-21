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

# The App Icon for browsers.
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'images/favicon.ico', mimetype='image/vnd.microsoft.icon')

# Redirect to the home-page by default.
@app.route("/")
def index():
    return redirect(url_for("BP_home.home"))

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