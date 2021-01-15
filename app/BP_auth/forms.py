# Classes for the Flask forms used in the authentication module.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField("Full Name", validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    cnf_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("CREATE MY ACCOUNT")

class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("LOGIN")