from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from app.models import User
from wtforms.validators import DataRequired, EqualTo


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password *", validators=[DataRequired()])
    new_password = PasswordField("New Password *", validators=[DataRequired()])
    confirm_new_password = PasswordField(
        "Confirm New Password *",
        validators=[DataRequired(), EqualTo("new_password")],
        render_kw={"onblur": "validatePassword()"},
    )
    submit = SubmitField("CHANGE PASSWORD")