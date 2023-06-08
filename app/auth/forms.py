from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Email, Length, Regexp, EqualTo

from .. import db
from ..models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = StringField("email", validators=[InputRequired(), Length(1, 64), Email()])
    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(1, 64),
            Regexp("^[A-Za-z]*$", 0, "Username must have only letters")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            EqualTo("password2", message="Password must match.")
        ]
    )
    password2 = PasswordField("Confirm password", validators=[InputRequired()])
    submit = SubmitField("Register")

    @staticmethod
    def validate_email(field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")

    @staticmethod
    def validate_username(field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use.")
