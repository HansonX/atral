from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, BooleanField, SubmitField, validators

class PatientRegistrationForm(FlaskForm):
    first_name = StringField('First Name', [validators.DataRequired(), validators.Length(min=4, max=25)])
    last_name = StringField('Last Name', [validators.DataRequired(), validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=4, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6, max=35)])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.EqualTo('password', message='Passwords must match')])
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField('Register')

class PhysicianRegistrationForm(FlaskForm):
    first_name = StringField('First Name', [validators.DataRequired(), validators.Length(min=4, max=25)])
    last_name = StringField('Last Name', [validators.DataRequired(), validators.Length(min=4, max=25)])
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

class PatientAssessmentForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    age = IntegerField('Age', [validators.DataRequired()])
    height = IntegerField('Height', [validators.DataRequired()])
    weight = IntegerField('Weight', [validators.DataRequired()])
    gender = BooleanField('Gender')
    is_smoker = BooleanField('Smoker status')
    is_drinker = BooleanField('Drinker status')
    is_active = BooleanField('Activity status')
    submit = SubmitField('Submit assessment')

class PhysicianAssessmentForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    sys_bp = StringField('Systolic BP', [validators.DataRequired()])
    dia_bp = StringField('Diastolic BP', [validators.DataRequired()])
    chol = StringField('Cholesterol', [validators.DataRequired()])
    glucose = StringField('Glucose',[validators.DataRequired()])
    submit = SubmitField('Submit assessment')
