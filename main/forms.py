from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.models import User, Groups

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max = 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max = 40)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max = 40), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max = 40)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max = 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    bio = StringField('Bio',validators=[Length(min=0, max=255)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max = 40)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max = 40), EqualTo('password')])
    submit = SubmitField('Reset Password')

class ListForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class NewGroup(FlaskForm):
    groupname = StringField('Group Name', validators=[DataRequired(),Length(min=2, max = 20)])
    bio = StringField('Bio',validators=[Length(min=0, max=255)])
    picture = FileField('Upload Group Picture', validators=[FileAllowed(['jpg','png'])])
    public = BooleanField('Public')
    submit = SubmitField('Sign Up')

    def validate_groupname(self, groupname):
        group = Groups.query.filter_by(groupname=groupname.data).first()
        if group:
            raise ValidationError('That group name is taken. Please choose a different one.')
