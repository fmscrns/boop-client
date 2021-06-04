from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_wtf.file import FileField, FileAllowed

class CreateCircleForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(max=30, message="Too long.")])
    bio_input = TextAreaField("Bio", validators=[Length(max=50, message="Too long.")])
    type_input = SelectMultipleField("Type", coerce=str, choices=[], validators=[InputRequired()])
    photo_input = FileField("Profile photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit_input = SubmitField("Create circle")

class EditCircleForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(max=30, message="Too long.")])
    bio_input = TextAreaField("Bio", validators=[Length(max=50, message="Too long.")])
    type_input = SelectMultipleField("Type", coerce=str, choices=[], validators=[InputRequired()])
    photo_input = FileField("Profile photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit_input = SubmitField("Update circle")

class JoinCircleForm(FlaskForm):
    submit_input = SubmitField("Join circle")

class LeaveCircleForm(FlaskForm):
    member_input = StringField()
    name_input = StringField("Name", validators=[DataRequired(), Length(max=30, message="Too long.")])
    confirm_name_input = StringField()
    submit_input = SubmitField()

class AcceptCircleForm(FlaskForm):
    member_input = StringField()
    submit_input  = SubmitField("Accept")

class DeleteCircleForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(max=30, message="Too long.")])
    confirm_name_input = StringField()
    submit_input = SubmitField("Delete circle")