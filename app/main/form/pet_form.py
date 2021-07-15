from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField

class CreatePetForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(min=2, max=30)])
    bio_input = TextAreaField("Bio", validators=[Length(min=2, max=50)])
    birthday_input = DateField("Birthday", format="%Y-%m-%d")
    sex_input = RadioField("Sex", coerce=int, choices=[(0, "Male"), (1, "Female")], validators=[InputRequired()])
    private_input = RadioField("Private", coerce=int, choices=[(1, "Yes"), (0, "No")], validators=[InputRequired()])
    group_input = SelectField("Specie", coerce=str, choices=[], validators=[InputRequired()])
    subgroup_input = SelectField("Breed", coerce=str, choices=[], validators=[InputRequired()])
    photo_input = FileField("Profile photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit_input = SubmitField("Create pet")

class EditPetForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(min=2, max=30)])
    bio_input = TextAreaField("Bio", validators=[Length(max=50)])
    birthday_input = DateField("Birthday", format="%Y-%m-%d")
    status_input = RadioField("Status", coerce=int, choices=[(0, "Closed"), (1, "Open for adoption"), (2, "Deceased")], validators=[InputRequired()])
    sex_input = RadioField("Sex", coerce=int, choices=[(0, "Male"), (1, "Female")], validators=[InputRequired()])
    private_input = RadioField("Private", coerce=int, choices=[(1, "Yes"), (0, "No")], validators=[InputRequired()])
    photo_input = FileField("Profile photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit_input = SubmitField("Update pet")

class DeletePetForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(min=2, max=30), EqualTo("confirm_name_input", message='Name must match.')])
    confirm_name_input = StringField()
    submit_input = SubmitField("Delete pet")

class FollowPetForm(FlaskForm):
    submit_input = SubmitField("Follow pet")

class UnfollowPetForm(FlaskForm):
    follower_input = StringField()
    submit_input = SubmitField()

class AcceptPetForm(FlaskForm):
    follower_input = StringField()
    submit_input  = SubmitField("Accept")

class CreatePetOwnerForm(FlaskForm):
    name_input = StringField(validators=[DataRequired()])
    owner_input = StringField()
    submit_input  = SubmitField("Add")

class DeletePetOwnerForm(FlaskForm):
    owner_input = StringField()
    confirm_name_input = StringField()
    name_input = StringField("Name", validators=[DataRequired(), Length(min=2, max=30), EqualTo("confirm_name_input", message='Name must match.')])
    submit_input  = SubmitField("Remove")