from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.core import SelectMultipleField
from wtforms.validators import InputRequired

class CreatePreferenceForm(FlaskForm):
    specie_group_input = SelectMultipleField("Specie", coerce=str, choices=[], validators=[InputRequired()])
    breed_subgroup_input = SelectMultipleField("Breed", coerce=str, choices=[], validators=[InputRequired()])
    business_type_input = SelectMultipleField("Business", coerce=str, choices=[], validators=[InputRequired()])
    circle_type_input = SelectMultipleField("Circle", coerce=str, choices=[], validators=[InputRequired()])
    
    submit_input = SubmitField("Create preference")