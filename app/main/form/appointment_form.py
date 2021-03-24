from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, EqualTo
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField

class CreateAppointmentForm(FlaskForm):
    details_input = TextAreaField("Details", validators=[Length(max=50, message="Too long.")])
    type_input = SelectMultipleField("Type", coerce=str, choices=[], validators=[InputRequired()])
    pet_input = SelectMultipleField("Pet", coerce=int, choices=[], validators=[InputRequired()])

    submit_input = SubmitField("Create appointment")

class EditAppointmentForm(FlaskForm):
    details_input = TextAreaField("Details", validators=[Length(max=50, message="Too long.")])
    type_input = SelectMultipleField("Type", coerce=str, choices=[], validators=[InputRequired()])
    pet_input = SelectMultipleField("Pet", coerce=int, choices=[], validators=[InputRequired()])

    submit_input = SubmitField("Edit appointment")

class DeleteAppointmentForm(FlaskForm):
    submit_input = SubmitField("Delete appointment")