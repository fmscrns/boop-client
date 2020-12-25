from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class CreateSpecieForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2, message="Too short.")])
    
    submit_input = SubmitField("Create")

class EditSpecieForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2, message="Too short.")])
    
    submit_input = SubmitField("Edit")

class DeleteSpecieForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2, message="Too short."), EqualTo("confirm_name_input", message='Name must match')])
    confirm_name_input = StringField("The Name", default="")
    submit_input = SubmitField("Delete")