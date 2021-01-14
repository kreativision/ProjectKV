from app.BP_auth import BP_auth
from app.BP_auth.forms import LoginForm, RegistrationForm
from flask.templating import render_template
from markupsafe import Markup
from flask.helpers import flash
from flask import redirect, url_for

@BP_auth.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", page="Login. . .", form=form)


@BP_auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        message = Markup(f'Account created for <strong>{form.username.data}</strong>! <br> You can now login with your <em>email</em> and <em>password</em>.')
        flash(message, category='success')
        return redirect(url_for('BP_auth.login'))
    return render_template("register.html", title="Create Account", page="Register", form=form)

@BP_auth.route("/forgot-password")
def recovery():
    return render_template('pwd-recovery.html', title="Account Recovery", page="Recover Account")