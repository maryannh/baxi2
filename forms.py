from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class join(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    first_name = StringField('firstname', validators=[DataRequired()]) 
    last_name = StringField('lastname', validators=[DataRequired()]) 
    learner_name = StringField('learner_name', validators=[DataRequired()]) 
    email = StringField('email', validators=[DataRequired()]) 