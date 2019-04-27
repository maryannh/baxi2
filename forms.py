from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, NoneOf
from functions import get_users

class JoinForm(FlaskForm):
    username = StringField('Username', validators=[NoneOf(get_users(), message="This username is already in use, please pick another one")])
    password = PasswordField('Password', validators=[Length(min=8, message="Please make sure your password has eight letters or more")])
    learner_name = StringField('Learner Name', validators=[DataRequired()]) 
    email = StringField('Email', validators=[Email()]) 