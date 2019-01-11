from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, email


class NewUserForm(FlaskForm):
    firstName = StringField('First Name')
    lastName = StringField('Last Name')
    username = StringField('Username')
    password = PasswordField('Password')
    email = StringField('Email')
    submit = SubmitField('Register New User')
