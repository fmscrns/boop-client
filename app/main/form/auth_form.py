from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class GetAuthTokenForm(FlaskForm):
    username_or_email_input = StringField("Username or email", default="", validators=[DataRequired()])
    password_input = PasswordField("Password", default="", validators=[DataRequired(), Length(min=6, message="Too short.")])

    submit_input = SubmitField("Sign in")