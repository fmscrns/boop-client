from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed

class CreateCommentForm(FlaskForm):
    content_input = TextAreaField("Content", validators=[Length(max=280)])
    photo_input = FileField("Photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    
    submit_input = SubmitField("Create comment")

class DeleteCommentForm(FlaskForm):
    submit_input = SubmitField("Delete post")