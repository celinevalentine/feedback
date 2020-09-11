from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, NumberRange, Optional, email_validator

class RegisterForm(FlaskForm):
    """form for registering a user"""

    username = StringField("Username", validators=[InputRequired(), Length(min=6, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=50)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(),Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(),Length(max=30)])



class LoginForm(FlaskForm):
    """form for login a user"""
    username = StringField("Username", validators=[InputRequired(), Length(min=6, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=50)])

class FeedbackForm(FlaskForm): 
    """form for adding feedback"""
    title = StringField("Title",validators=[InputRequired(),Length(max=100)])
    content = StringField("Content",validators=[InputRequired()])
    





class DeleteForm(FlaskForm):
    """reset form to blank"""
