from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed

class CreateUserForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2, message="Too short.")])
    username_input = StringField("Username", default="", validators=[DataRequired()])
    email_input = StringField("Email", default="", validators=[DataRequired(), Email("Invalid email.")])
    password_input = PasswordField("Password", default="", validators=[DataRequired(), Length(min=6, message="Too short.")])
    confirm_password_input = PasswordField("Confirm password", default="", validators=[DataRequired(), Length(min=6, message="Too short."), EqualTo("password_input")])

    submit_input = SubmitField("Sign up")

class EditUserForm(FlaskForm):
    photo_input = FileField("Photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2, message="Too short.")])
    username_input = StringField("Username", default="", validators=[DataRequired()])
    email_input = StringField("Email", default="", validators=[DataRequired(), Email("Invalid email.")])
    password_input = PasswordField("Password", default="", validators=[DataRequired(), Length(min=6, message="Too short.")])
    confirm_password_input = PasswordField("Confirm password", default="", validators=[DataRequired(), Length(min=6, message="Too short."), EqualTo("password_input")])

    submit_input = SubmitField("Edit profile")