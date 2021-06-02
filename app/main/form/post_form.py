from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, EqualTo
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField

class CreatePostForm(FlaskForm):
    content_input = TextAreaField("Content", validators=[Length(max=280, message="Too long.")])
    photo_input = FileField("Photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    pinboard_input = StringField()
    confiner_input = StringField()

    submit_input = SubmitField("Create post")

class DeletePostForm(FlaskForm):
    submit_input = SubmitField("Delete post")