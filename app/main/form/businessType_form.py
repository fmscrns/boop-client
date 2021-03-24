from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class CreateBusinessTypeForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2, message="Too short.")])
    
    submit_input = SubmitField("Create business type")

class EditBusinessTypeForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2, message="Too short.")])
    
    submit_input = SubmitField("Update business type")

class DeleteBusinessTypeForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2, message="Too short."), EqualTo("confirm_name_input", message='Name must match')])
    confirm_name_input = StringField("The Name", default="")
    submit_input = SubmitField("Delete business type")