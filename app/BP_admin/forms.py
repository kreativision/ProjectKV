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
from app import encryptor
from flask_login import current_user


class EditAdminDetailsForm(FlaskForm):
    username = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=3, max=50, message="Name must be 3 to 50 characters long"),
        ],
    )
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    contact = IntegerField(
        "Contact",
        validators=[
            DataRequired(),
            NumberRange(
                min=1000000000,
                max=9999999999,
                message="Contact number should have 10 digits (no spaces)",
            ),
        ],
        render_kw={"inputmode": "numeric", "minlength": "10", "maxlength": "10"},
    )
    password = PasswordField("Password *", validators=[DataRequired()])
    submit = SubmitField("Save Changes")

    def validate_password(self, password):
        user = User.query.filter_by(email=current_user.email).first()
        if not encryptor.check_password_hash(user.password, self.password.data):
            raise ValidationError("Incorrect Password")


class EditAdminPasswordForm(FlaskForm):
    current_password = PasswordField("Current Password *", validators=[DataRequired()])
    new_password = PasswordField("New Password *", validators=[DataRequired()])
    confirm_new_password = PasswordField(
        "Confirm New Password *",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"onkeyup": "validatePassword()"},
    )
    submit = SubmitField("Change Password")
