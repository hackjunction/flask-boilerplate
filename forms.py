from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, Length

class CompanyForm(Form):
    name = TextField(
        'Company Name', validators=[DataRequired(), Length(min=1, max=50)]
    )
    contact_email = TextField(
        'Contact Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    excellent_skills = SelectMultipleField('Skills applicant should excel at')
    extra_skills = SelectMultipleField('Skills applicant should excel at')

class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
