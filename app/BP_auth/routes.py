from flask_login import login_user, logout_user, current_user
from flask import redirect, url_for, flash, render_template, request, jsonify
from markupsafe import Markup
from app import db, encryptor, mail
import app.utils as utils
from app.models import User
from app.BP_auth import BP_auth
from app.BP_auth.forms import (
    LoginForm,
    RegistrationForm,
    RequestResetPasswordForm,
    ResetPasswordForm,
)

@BP_auth.route("/test")
def test():
    return render_template("new-password.html", form=ResetPasswordForm())

# Login User
@BP_auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        content = [f"Session Active", f"You are already logged in."]
        flash(content, category="info")
        return redirect(url_for("BP_home.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and encryptor.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.admin:
                return redirect(url_for("BP_admin.home"))
            content = [f"Login Successful", f"You have been successfully logged in."]
            flash(content, category="success")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect (url_for("BP_home.home"))
        else:
            content = [
                f"Login Failed.",
                Markup(f"<strong>Incorrect credentials</strong>.<br>Please try again!"),
            ]
            flash(content, category="danger")
    return render_template("login.html", title="Login", page="Login. . .", form=form)


# Logout User
@BP_auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("BP_home.home"))

# Register new user
@BP_auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        content = [f"Session Active", f"You are already logged in."]
        flash(content, category="info")
        return redirect(url_for("BP_home.home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user_name = form.username.data.title()
        user_password = encryptor.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        new_user = User(
            username=user_name,
            email=form.email.data,
            password=user_password,
            contact=form.contact.data,
        )
        db.session.add(new_user)
        db.session.commit()
        register_token = new_user.generate_token()
        utils.send_email(
            "Activate Account: KreatiVision",
            "picskreativision@gmail.com",
            [new_user.email],
            render_template(
                "registration-mail.txt", token=register_token, name=new_user.username
            ),
            render_template(
                "registration-mail.html", token=register_token, name=new_user.username
            ),
        )
        return render_template(
            "email-sent.html",
            title="Activate Account",
            mail=utils.redact_email(new_user.email),
            case="register",
        )
    return render_template(
        "register.html", title="Create Account", page="Register", form=form
    )


@BP_auth.route("/verify-account/<token>")
def verify_account(token):
    if current_user.is_authenticated:
        content = [f"Session Active", f"Go to My Account page to change your password"]
        flash(content, category="info")
        return redirect(url_for("BP_home.home"))
    user = User.verify_token(token)
    if user is None:
        content = [
            f"Link Expired or Invalid",
            f"The Activation link is either invalid or expired, please try again",
        ]
        flash(content, category="danger")
        # Redirect to account info page for reconfirmation.
        return redirect(url_for("BP_home.home"))
    user.verified = True
    db.session.commit()
    content = [
        f"Account Created!",
        Markup(
            f"Welcome {user.username}.<br>Please login using your <strong>email</strong> and <strong>password</strong>."
        ),
    ]
    flash(content, category="success")
    return redirect(url_for("BP_auth.login"))


# Password Recovery Request
@BP_auth.route("/forgot-password", methods=["GET", "POST"])
def reset_request():
    # redirect to home if session is active
    if current_user.is_authenticated:
        content = [f"Session Active", f"Go to My Account page to change your password"]
        flash(content, category="info")
        return redirect(url_for("BP_home.home"))
    # to password reset request page
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.generate_token()
        # using background method from utils to send email
        utils.send_email(
            "Password Reset: KreatiVision",
            "picskreativision@gmail.com",
            [user.email],
            render_template("reset-mail-body.txt", token=token, name=user.username),
            render_template("reset-mail-body.html", token=token, name=user.username),
        )
        return render_template(
            "email-sent.html",
            title="Reset Password",
            mail=utils.redact_email(user.email),
            case="reset",
        )
    # if mail doesn't exist on db
    return render_template(
        "pwd-recovery.html",
        title="Password Reset",
        page="Request Password Reset",
        form=form,
    )


# Verify password reset token and change password
@BP_auth.route("/forgot-password/<token>", methods=["GET", "POST"])
def reset_token(token):
    # redirect to home if session is active
    if current_user.is_authenticated:
        content = [f"Session Active", f"Go to My Account page to change your password"]
        flash(content, category="info")
        return redirect(url_for("BP_home.home"))
    # verification
    user = User.verify_token(token)
    # if invalid/expired token
    if user is None:
        content = [
            f"Link Expired or Invalid",
            f"The reset link is either invalid or expired, please try again",
        ]
        flash(content, category="danger")
        return redirect(url_for("BP_auth.reset_request"))
    # If valid token
    form = ResetPasswordForm()
    # if new password form valid
    if form.validate_on_submit():
        user_password = encryptor.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = user_password
        db.session.commit()
        content = [
            f"Password changes successfully!",
            f"Please login user your email and new password",
        ]
        flash(content, category="success")
        return redirect(url_for("BP_auth.login"))
    return render_template(
        "new-password.html",
        title="Create New Password",
        page="Create New Password",
        form=form,
    )

@BP_auth.route("/api/check-email/<string:email_id>", methods=["GET"])
def check_email(email_id):
    print(email_id)
    is_user = User.query.filter_by(email=email_id).first()
    if is_user:
        return jsonify({"registered": 1})
    else:
        return jsonify({"registered": 0})