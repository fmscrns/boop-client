from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed

class CreatePostForm(FlaskForm):
    content_input = TextAreaField("Content", validators=[Length(min=1, max=280)])
    photo_input = FileField("Photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    pinboard_input = StringField()
    confiner_input = StringField()
    subject_input = SelectMultipleField("Tag pets", coerce=str, choices=[], validators=[InputRequired()])

    submit_input = SubmitField("Create post")

class DeletePostForm(FlaskForm):
    submit_input = SubmitField("Delete post")