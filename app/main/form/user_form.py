from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from ..service.user_service import UserService

class CreateUserOneForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2)])
    email_input = StringField("Email", default="", validators=[DataRequired(), Email("Invalid email.")])

    submit_input = SubmitField("Next")

    def validate_email_input(self, email_input):
        api_resp = UserService.get_by_email(email_input.data)

        if api_resp:
            raise ValidationError("This email has already been taken.")

class CreateUserTwoForm(FlaskForm):
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2)])
    email_input = StringField("Email", default="", validators=[DataRequired(), Email("Invalid email.")])
    username_input = StringField("Username", default="", validators=[DataRequired()])
    password_input = PasswordField("Password", default="", validators=[DataRequired(), Length(min=6)])
    confirm_password_input = PasswordField("Confirm password", default="", validators=[DataRequired(), Length(min=6), EqualTo("password_input")])

    submit_input = SubmitField("Sign up")

class EditUserForm(FlaskForm):
    photo_input = FileField("Photo", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    name_input = StringField("Name", default="", validators=[DataRequired(), Length(min=2)])
    username_input = StringField("Username", default="", validators=[DataRequired()])
    email_input = StringField("Email", default="", validators=[DataRequired(), Email("Invalid email.")])
    password_input = PasswordField("Password", default="", validators=[DataRequired(), Length(min=6)])
    confirm_password_input = PasswordField("Confirm password", default="", validators=[DataRequired(), Length(min=6), EqualTo("password_input")])

    submit_input = SubmitField("Update profile")