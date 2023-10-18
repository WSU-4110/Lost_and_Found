from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, ValidationError, Length
from app.models import User


# Create a LoginForm class that inherits from FlaskForm
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=20)])
    submit = SubmitField('Sign In')

# Create a RegistrationForm class that inherits from FlaskForm
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=20)])
    submit = SubmitField('Sign Up')

    # Create a custom validation method to check if the username is already taken
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(f'Username {username.data} is already taken. Please choose a different one.')
    
    # Create a custom validation method to check if the email is already taken
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(f'Email {email.data} is already taken. Please choose a different one.')
        if not email.data.endswith('@wayne.edu'):
            raise ValidationError(f'Email {email.data} is not valid. Please use a Wayne State University Email Address.')