from app import encryptor
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms.fields.core import IntegerField, StringField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    ValidationError,
)
from wtforms.fields.simple import PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed

# form prefixes to generate unique ID's for form elements.
prefix = {"info": "detailsForm", "pwd": "passwordForm", "dp": "dpForm"}

# Update Account Details Form
class UpdateAccountInfoForm(FlaskForm):
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
        if not encryptor.check_password_hash(current_user.password, password.data):
            raise ValidationError("Incorrect Password")


# Change User Password Form
class ChangeUserPasswordForm(FlaskForm):
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


# Change Profile Picture Form
class UpdateDPForm(FlaskForm):
    dp_image = FileField(
        "Change",
        validators=[FileAllowed(["jpeg", "jpg", "png"])],
        render_kw={"accept": ".png,.jpg,.jpeg"},
    )
    submitDp = SubmitField("Upload")