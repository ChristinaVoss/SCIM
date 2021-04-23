#form imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

#user imports
from flask_login import current_user
from schoolclubinfomanager.models import User

# Flask forms allow you to easily create forms in format:
# variable_name = Field_type('Label that will show', validators=[V_func1(), V_func2(),...])
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    # Check if that email address has already been registered
    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    name = StringField('Name')

    submit = SubmitField('Update details')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')

class DeleteUserForm(FlaskForm):

    submit = SubmitField('Delete User')
