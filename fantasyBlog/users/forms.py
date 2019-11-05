from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField #update avatar
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

from flask_login import current_user
from fantasyBlog.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email is already registered')
    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already in use')
    
    

class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    avatar = SelectField('Select avatar', choices=[])
    submit = SubmitField('Save')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email is already registered')
    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already in use')

class DisplayUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    avatar = FileField('Update avatar', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')
    