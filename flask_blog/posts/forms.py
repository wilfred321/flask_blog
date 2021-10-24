from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")


class CommentForm(FlaskForm):
    body = StringField(
        "Comment", validators=[DataRequired(), Length(min=10, max=100, message=None)]
    )
    submit = SubmitField("Reply")
