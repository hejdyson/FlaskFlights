from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


# class inherits from imported extension
# Registration form
class RegistrationForm(FlaskForm):              # cant be empty     # min max length
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # validation for valid email also from extension
    email = StringField('Email', validators=[DataRequired(), Email()])
    # passwords validation - confirm also has to be equal to our first password
    password = PasswordField('Password', validators=[DataRequired()])
    # EqualTo has to take STRING name of password!!!!! NOT JUST VARIABLE
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# form for updating account info
class UpdateAccountForm(FlaskForm):              # cant be empty     # min max length
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # validation for valid email also from extension
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


# reseting passwords
# first get email and validate it
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must create account first.')


# then putting old password for confirmation
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
