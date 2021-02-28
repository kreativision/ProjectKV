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

# Form for updating user details.
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
    submitInfo = SubmitField("Save Changes")

    def validate_password(self, password):
        user = User.query.filter_by(email=current_user.email).first()
        if not encryptor.check_password_hash(user.password, password.data):
            raise ValidationError("Incorrect Password")

# Form for updating user password
class EditAdminPasswordForm(FlaskForm):
    current = PasswordField("Current Password *", validators=[DataRequired()])
    new_password = PasswordField("New Password *", validators=[DataRequired()])
    confirm_new_password = PasswordField(
        "Confirm New Password *",
        validators=[DataRequired(), EqualTo("new_password")],
    )
    submitPwd = SubmitField("Change Password")

    def validate_current(self, current):
        user = User.query.filter_by(id=current_user.id).first()
        if not encryptor.check_password_hash(user.password, current.data):
            raise ValidationError("Incorrect Password")

    def validate_new_password(self, new_password):
        user = User.query.filter_by(id=current_user.id).first()
        if encryptor.check_password_hash(user.password, new_password.data):
            raise ValidationError("New password cannot be same as old password")