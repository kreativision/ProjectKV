from flask import Blueprint, redirect, flash, url_for
from markupsafe import Markup
from flask.templating import render_template
from BP_auth.forms import LoginForm, RegistrationForm

auth_bp = Blueprint(
    "auth_bp",
    __name__,
    template_folder="templates",
    static_folder="assets",
    static_url_path="/assets",
)

@auth_bp.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", page="Login. . .", form=form)


@auth_bp.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        message = Markup(f'Account Created for <strong>{form.username.data}</strong>!')
        flash(message, category='success')
        return redirect(url_for('auth_bp.login'))
    return render_template("register.html", title="Create Account", page="Register", form=form)
