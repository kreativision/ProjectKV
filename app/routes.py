# This is the global app routes file.
from flask import redirect, url_for
from app import app, db, encryptor
from app.models import User
from app.BP_auth.forms import LoginForm, RegistrationForm
from markupsafe import Markup
from flask.helpers import flash
from flask.templating import render_template
from flask_login import login_user, logout_user, current_user

# Redirect to the home-page by default.
@app.route("/")
def index():
    return redirect(url_for("BP_home.home"))

# Registration page
@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        message = Markup(f'You are already logged in.')
        flash(message, category='info')
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user_password = encryptor.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=user_password, contact=form.contact.data)
        db.session.add(new_user)
        db.session.commit()
        message = Markup(f'Welcome <strong>{form.username.data}</strong>! <br> Your account is created successfully.')
        flash(message, category='success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Create Account", page="Register", form=form)

# Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        message = Markup(f'You are already logged in.')
        flash(message, category='info')
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and encryptor.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            message = f'You have been logged in!'
            flash(message, category='primary')
            return redirect(url_for('index'))
        else:
            message = f'Incorrect credentials. Please try again!'
            flash(message, category='danger')
    return render_template("login.html", title="Login", page="Login. . .", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


# Password Recovery
@app.route("/forgot-password")
def recovery():
    return render_template('pwd-recovery.html', title="Account Recovery", page="Recover Account")