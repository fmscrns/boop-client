from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length

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