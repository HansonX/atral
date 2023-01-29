from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators

class PatientRegistrationForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=4, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6, max=35)])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.EqualTo('password', message='Passwords must match')])
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField('Register')

class PhysicianRegistrationForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=4, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6, max=35)])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.EqualTo('password', message='Passwords must match')])
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6, max=35)])
    submit = SubmitField('Log in')
