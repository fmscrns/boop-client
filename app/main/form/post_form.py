from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileAllowed

class CreatePostForm(FlaskForm):
    content_input = TextAreaField("Content", validators=[Length(min=1, max=280)])
    photos_fn_input = MultipleFileField(validators=[FileAllowed(["jpg", "jpeg", "png"])])
    photo_1_input = TextAreaField()
    photo_2_input = TextAreaField()
    photo_3_input = TextAreaField()
    photo_4_input = TextAreaField()
    pinboard_input = StringField()
    confiner_input = StringField()
    subject_input = SelectMultipleField("Tag pets", coerce=str, choices=[], validators=[InputRequired()])

    submit_input = SubmitField("Create post")

class DeletePostForm(FlaskForm):
    pinboard_input = StringField()
    confiner_input = StringField()
    submit_input = SubmitField("Delete post")

class LikePostForm(FlaskForm):
    submit_input = SubmitField("Like post")