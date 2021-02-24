# Classes for the Flask forms used in the authentication module.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Optional,
    ValidationError,
)
from markupsafe import Markup
from flask.helpers import url_for
from app.models import User


class RegistrationForm(FlaskForm):
    # render_kw => add autofocus feature.
    username = StringField(
        "Full Name *",
        validators=[
            DataRequired(),
            Length(min=3, max=50, message="Name must be 3 to 50 characters long"),
        ],
        render_kw={"autofocus": True},
    )
    email = StringField("E-mail *", validators=[DataRequired(), Email()])
    contact = IntegerField(
        "Contact *",
        validators=[
            DataRequired(),
            NumberRange(
                min=1000000000,
                max=9999999999,
                message="Contact number should have 10 digits (no spaces)",
            ),
        ],
        render_kw={"inputmode": "numeric", "minlength":"10","maxlength":"10"}
    )
    password = PasswordField("Password *", validators=[DataRequired()])
    cnf_password = PasswordField(
        "Confirm Password *",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"onkeyup": "validatePassword()"},
    )
    submit = SubmitField("CREATE MY ACCOUNT")
    # check if email in db
    def validate_email(self, email):
        user_mail = User.query.filter_by(email=email.data).first()
        if user_mail:
            message = Markup(
                f"This e-mail is already registered. You can <a href='{url_for('BP_auth.login')}'>login</a> or <a href='{url_for('BP_auth.reset_request')}'>reset your password</a>."
            )
            raise ValidationError(message)


class LoginForm(FlaskForm):
    email = StringField(
        "E-mail", validators=[DataRequired(), Email()], render_kw={"autofocus": True}
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("LOGIN")
    # check if email in db
    def validate_email(self, email):
        user_mail = User.query.filter_by(email=email.data).first()
        if not user_mail:
            message = Markup(
                f"This email is not registered. Please <a href='{url_for('BP_auth.sign_up')}'>register</a>."
            )
            raise ValidationError(message)


class RequestResetPasswordForm(FlaskForm):
    email = StringField(
        "E-mail", validators=[DataRequired(), Email()], render_kw={"autofocus": True}
    )
    submit = SubmitField("REQUEST RESET")

    def validate_email(self, email):
        user_mail = User.query.filter_by(email=email.data).first()
        if user_mail is None:
            message = Markup(
                f"This email is not registered. <a href='{url_for('BP_auth.sign_up')}'>Please register</a>."
            )
            raise ValidationError(message)


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password *", validators=[DataRequired()], render_kw={"autofocus": True}
    )
    cnf_password = PasswordField(
        "Confirm Password *", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("CHANGE PASSWORD")