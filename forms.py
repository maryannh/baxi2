from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length, NoneOf
from functions import get_users

class join(FlaskForm):
    username = StringField('username', validators=[NoneOf(get_users, message="This username is already in use, please pick another one")])
    password = StringField('password', validators=[Length(min=8, message="Please make sure your password has eight letters or more")])
    learner_name = StringField('learner_name', validators=[DataRequired()]) 
    email = StringField('email', validators=[Email()]) 