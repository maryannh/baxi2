from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, NoneOf, AnyOf
from functions import get_users, get_user_emails

class JoinForm(FlaskForm):
    username = StringField('Username', validators=[NoneOf(get_users(), message="This username is already in use, please pick another one")])
    password = PasswordField('Password', validators=[Length(min=8, message="Please make sure your password has eight letters or more")])
    learner_name = StringField('Learner Name', validators=[DataRequired()]) 
    email = StringField('Email', validators=[Email(), NoneOf(get_user_emails(), message="This email address is already in use, please check you are not already a member")]) 
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[AnyOf(get_users(), message="This username has not been recognised, please check it and try again")])
    password = PasswordField('Password', validators=[Length(min=8, message="Your password would have had eight letters or more")])