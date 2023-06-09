from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Email, Length, Regexp, EqualTo, DataRequired

from .. import db
from ..models import User


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            InputRequired(),
            Length(1, 64),
            Email(),
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
        ]
    )
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = StringField(
        "email",
        validators=[
            InputRequired(),
            Length(1, 64),
            Email(),
        ]
    )
    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(1, 64),
            Regexp("^[A-Za-z]*$", 0, "Username must have only letters"),
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            EqualTo(
                "password2",
                message="Password must match."
            ),
        ]
    )
    password2 = PasswordField(
        "Confirm password",
        validators=[
            InputRequired(),
        ]
    )
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use.")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        'Old password',
        validators=[
            DataRequired(),
        ]
    )
    password = PasswordField(
        'New password',
        validators=[
            DataRequired(),
            EqualTo(
                'password2',
                message='Passwords must match.'
            )
        ]
    )
    password2 = PasswordField(
        'Confirm new password',
        validators=[
            DataRequired(),
        ]
    )
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(1, 64),
            Email(),
        ]
    )
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            EqualTo(
                'password2',
                message='Passwords must match'
            ),
        ]
    )
    password2 = PasswordField(
        'Confirm password',
        validators=[DataRequired()]
    )
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    email = StringField(
        'New Email',
        validators=[DataRequired(), Length(1, 64), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')
