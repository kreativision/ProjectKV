from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from wtforms.validators import DataRequired, Optional
from wtforms.fields.simple import SubmitField, TextAreaField


class EditReviewForm(FlaskForm):
    review_title = StringField(
        "Review Title *", validators=[DataRequired()], render_kw={"maxlength": "140"}
    )
    review_content = TextAreaField("Review Content", validators=[Optional()], render_kw={"rows": "8"})
    submit_review = SubmitField("Save")