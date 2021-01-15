# Classes for the Flask forms used in the authentication module.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from markupsafe import Markup
from flask.helpers import url_for
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Full Name", validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    cnf_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("CREATE MY ACCOUNT")
    # Check for email already in the database.
    def validate_email(self, email):
        user_mail = User.query.filter_by(email=email.data).first()
        if user_mail:
            message = Markup(f"This e-mail is already registered. You can <a href='{url_for('login')}'>login</a> or <a href='{url_for('recovery')}'>reset your password</a>.")
            raise ValidationError(message)

class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("LOGIN")