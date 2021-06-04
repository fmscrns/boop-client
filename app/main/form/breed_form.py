from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo


class CreateBreedForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2, message="Too short.")])
    parent_input = SelectField("Specie", coerce=str, choices=[], validators=[InputRequired()])
    submit_input = SubmitField("Create breed")

class EditBreedForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2, message="Too short.")])
    parent_input = SelectField("Specie", coerce=str, choices=[], validators=[InputRequired()])
    submit_input = SubmitField("Update breed")

class DeleteBreedForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2, message="Too short."), EqualTo("confirm_name_input", message='Name must match')])
    confirm_name_input = StringField("The Name", default="")
    parent_input = SelectField("Specie", coerce=str, choices=[], validators=[InputRequired()])
    submit_input = SubmitField("Delete breed")