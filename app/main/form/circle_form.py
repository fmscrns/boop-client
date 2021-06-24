from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed

class CreateCircleForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(min=2, max=30)])
    bio_input = TextAreaField("Bio", validators=[Length(max=50)])
    type_input = SelectMultipleField("Type", coerce=str, choices=[], validators=[InputRequired()])
    photo_input = FileField("Profile photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit_input = SubmitField("Create circle")

class EditCircleForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(min=2, max=30)])
    bio_input = TextAreaField("Bio", validators=[Length(max=50)])
    type_input = SelectMultipleField("Type", coerce=str, choices=[], validators=[InputRequired()])
    photo_input = FileField("Profile photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit_input = SubmitField("Update circle")

class JoinCircleForm(FlaskForm):
    submit_input = SubmitField("Join circle")

class LeaveCircleForm(FlaskForm):
    member_input = StringField()
    submit_input = SubmitField()

class AcceptCircleForm(FlaskForm):
    member_input = StringField()
    submit_input  = SubmitField("Accept")

class DeleteCircleForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(min=2, max=30), EqualTo("confirm_name_input", message='Name must match.')])
    confirm_name_input = StringField()
    submit_input = SubmitField("Delete circle")

class CreateCircleAdminForm(FlaskForm):
    name_input = StringField(validators=[DataRequired()])
    admin_input = StringField()
    submit_input  = SubmitField("Make admin")

class DeleteCircleAdminForm(FlaskForm):
    admin_input = StringField()
    confirm_name_input = StringField()
    name_input = StringField("Name", validators=[DataRequired(), Length(min=2, max=30), EqualTo("confirm_name_input", message='Name must match.')])
    submit_input  = SubmitField("Remove")