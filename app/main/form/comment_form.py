from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed

class CreateCommentForm(FlaskForm):
    content_input = TextAreaField("Content", validators=[Length(min=1, max=280)])
    photo_input = FileField("Photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    parent_input = StringField()
    submit_input = SubmitField("Create comment")

class DeleteCommentForm(FlaskForm):
    parent_input = StringField()
    submit_input = SubmitField("Delete comment")