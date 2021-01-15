from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, EqualTo
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField

class CreateBusinessForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(max=30, message="Too long.")])
    bio_input = TextAreaField("Bio", validators=[Length(max=50, message="Too long.")])
    type_input = SelectMultipleField("Type", coerce=int, choices=[(0, "Grooming"), (1, "Veterinary clinic"), (2, "Supply and accessories")], validators=[InputRequired()])
    photo_input = FileField("Profile photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit_input = SubmitField("Create business")

class EditBusinessForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(max=30, message="Too long.")])
    bio_input = TextAreaField("Bio", validators=[Length(max=50, message="Too long.")])
    type_input = SelectMultipleField("Type", coerce=int, choices=[(0, "Grooming"), (1, "Veterinary clinic"), (2, "Supply and accessories")], validators=[InputRequired()])
    photo_input = FileField("Profile photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit_input = SubmitField("Update business")

class DeleteBusinessForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(max=30, message="Too long.")])
    confirm_name_input = StringField("The Name", default="")
    submit_input = SubmitField("Delete business")