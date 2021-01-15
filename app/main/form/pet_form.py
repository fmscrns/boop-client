from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, EqualTo
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField

class CreatePetForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(max=30, message="Too long.")])
    bio_input = TextAreaField("Bio", validators=[Length(max=50, message="Too long.")])
    birthday_input = DateField("Birthday", format="%Y-%m-%d")
    sex_input = RadioField("Sex", coerce=int, choices=[(0, "Male"), (1, "Female")], validators=[InputRequired()])
    group_input = SelectField("Specie", coerce=str, choices=[], validators=[InputRequired()])
    subgroup_input = SelectField("Breed", coerce=str, choices=[], validators=[InputRequired()])
    photo_input = FileField("Profile photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit_input = SubmitField("Create pet")

class EditPetForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2, message="Too short.")])
    bio_input = TextAreaField("Bio", validators=[Length(max=50, message="Too long.")])
    birthday_input = DateField("Birthday", format="%Y-%m-%d")
    status_input = RadioField("Status", coerce=int, choices=[(0, "Closed"), (1, "Open for adoption")], validators=[InputRequired()])
    sex_input = RadioField("Sex", coerce=int, choices=[(0, "Male"), (1, "Female")], validators=[InputRequired()])
    photo_input = FileField("Profile photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit_input = SubmitField("Update pet")

class DeletePetForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2, message="Too short."), EqualTo("confirm_name_input", message='Name must match')])
    confirm_name_input = StringField("The Name", default="")
    submit_input = SubmitField("Delete pet")