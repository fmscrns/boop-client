from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class CreateSpecieForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(min=2, message="Too short.")])
    
    submit_input = SubmitField("Create specie")

class EditSpecieForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(min=2, message="Too short.")])
    
    submit_input = SubmitField("Update specie")

class DeleteSpecieForm(FlaskForm):
    name_input = StringField("Name", validators=[DataRequired(), Length(min=2, message="Too short."), EqualTo("confirm_name_input", message='Name must match')])
    confirm_name_input = StringField()
    submit_input = SubmitField("Delete specie")