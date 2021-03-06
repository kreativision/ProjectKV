from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerField,
    TextAreaField,
)
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
from flask_login import current_user
from app import encryptor


class UpdateForm(FlaskForm):
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
        render_kw={"inputmode": "numeric", "minlength": "10", "maxlength": "10"},
    )
    password = PasswordField("Password *", validators=[DataRequired()])
    submitInfo = SubmitField("Save Changes")

    def validate_password(self, password):
        if not encryptor.check_password_hash(current_user.password, password.data):
            raise ValidationError("Incorrect Password")


# Form for updating user password
class PasswordForm(FlaskForm):
    current = PasswordField("Current Password *", validators=[DataRequired()])
    new_password = PasswordField("New Password *", validators=[DataRequired()])
    confirm_new_password = PasswordField(
        "Confirm New Password *",
        validators=[DataRequired(), EqualTo("new_password")],
    )
    submitPwd = SubmitField("Change Password")

    def validate_current(self, current):
        if not encryptor.check_password_hash(current_user.password, current.data):
            raise ValidationError("Incorrect Password")

    def validate_new_password(self, new_password):
        if encryptor.check_password_hash(current_user.password, new_password.data):
            raise ValidationError("New password cannot be same as old password")


class CustomizeServiceForm(FlaskForm):
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    preferences = TextAreaField(
        "Specific Requirements (if any)", validators=[Optional()], render_kw={"rows": "4"}
    )