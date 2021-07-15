from app.main.form import AttribSelectMultipleField
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.core import SelectMultipleField
from wtforms.validators import InputRequired

class CreatePetPreferenceForm(FlaskForm):
    specie_group_input = SelectMultipleField("Specie", coerce=str, choices=[])
    breed_subgroup_input = AttribSelectMultipleField("Breed", coerce=str, choices=[], validators=[InputRequired()])

    submit_input = SubmitField("Update pet preference")

class CreateBusinessPreferenceForm(FlaskForm):
    business_type_input = AttribSelectMultipleField("Business", coerce=str, choices=[], validators=[InputRequired()])

    submit_input = SubmitField("Update business preference")

class CreateCirclePreferenceForm(FlaskForm):
    circle_type_input = AttribSelectMultipleField("Circle", coerce=str, choices=[], validators=[InputRequired()])
    
    submit_input = SubmitField("Update circle preference")