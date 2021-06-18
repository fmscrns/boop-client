from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, EqualTo
from flask_wtf.file import FileField, FileAllowed
from wtforms_components import TimeField

def round_hour_check(form, field):
    if not field.data.minute == field.data.second == field.data.microsecond == 0:
        raise ValidationError('This should be a round hour.')

class CreateBusinessForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(max=30)])
    bio_input = TextAreaField("Bio", validators=[Length(max=50)])
    type_input = SelectMultipleField("Type", coerce=str, choices=[], validators=[InputRequired()])

    mon_open_bool = BooleanField("Monday")
    mon_open_time = TimeField('Monday opening time', validators=[round_hour_check])
    mon_close_time = TimeField('Monday closing time', validators=[round_hour_check])

    tue_open_bool = BooleanField("Tuesday")
    tue_open_time = TimeField('Tuesday opening time', validators=[round_hour_check])
    tue_close_time = TimeField('Tuesday closing time', validators=[round_hour_check])

    wed_open_bool = BooleanField("Wednesday")
    wed_open_time = TimeField('Wednesday opening time', validators=[round_hour_check])
    wed_close_time = TimeField('Wednesday closing time', validators=[round_hour_check])

    thu_open_bool = BooleanField("Thursday")
    thu_open_time = TimeField('Thursday opening time', validators=[round_hour_check])
    thu_close_time = TimeField('Thursday closing time', validators=[round_hour_check])

    fri_open_bool = BooleanField("Friday")
    fri_open_time = TimeField('Friday opening time', validators=[round_hour_check])
    fri_close_time = TimeField('Friday closing time', validators=[round_hour_check])

    sat_open_bool = BooleanField("Saturday")
    sat_open_time = TimeField('Saturday opening time', validators=[round_hour_check])
    sat_close_time = TimeField('Saturday closing time', validators=[round_hour_check])

    sun_open_bool = BooleanField("Sunday")
    sun_open_time = TimeField('Sunday opening time', validators=[round_hour_check])
    sun_close_time = TimeField('Sunday closing time', validators=[round_hour_check])

    photo_input = FileField("Profile photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    sessions_input = SelectMultipleField("Sessions", coerce=str, choices=[])

    submit_input = SubmitField("Create business")

class EditBusinessForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(max=30)])
    bio_input = TextAreaField("Bio", validators=[Length(max=50)])
    type_input = SelectMultipleField("Type", coerce=str, choices=[], validators=[InputRequired()])
    photo_input = FileField("Profile photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit_input = SubmitField("Update business")

class DeleteBusinessForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(max=30), EqualTo("confirm_name_input", message='Name must match.')])
    confirm_name_input = StringField()
    submit_input = SubmitField("Delete business")

class FollowBusinessForm(FlaskForm):
    submit_input = SubmitField("Follow business")

class UnfollowBusinessForm(FlaskForm):
    follower_input = StringField()
    submit_input = SubmitField()

class CreateBusinessExecutiveForm(FlaskForm):
    executive_input = StringField()
    submit_input  = SubmitField("Add")

class DeleteBusinessExecutiveForm(FlaskForm):
    executive_input = StringField()
    confirm_name_input = StringField()
    name_input = StringField("Name", validators=[DataRequired(), Length(min=2, max=30), EqualTo("confirm_name_input", message='Name must match.')])
    submit_input  = SubmitField("Remove")