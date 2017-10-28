from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length

# Multiselect field without validation
class NoValidationSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        """per_validation is disabled"""
        return True


class CompanyForm(Form):
    name = TextField(
        'Company Name', validators=[DataRequired(), Length(min=1, max=50)]
    )

    time_present = TextField(
        'Time present', validators=[DataRequired(), Length(min=1, max=100)]
    )

    contact_email = TextField(
        'Contact Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    excellent_skills = NoValidationSelectMultipleField('Skills applicant should excel at')
    extra_skills = NoValidationSelectMultipleField('Skills applicant should excel at')
    titles = NoValidationSelectMultipleField('Job titles you are hiring for')

    amount_meetings = IntegerField('How many meetings with applicants do you wish to have?')
    personnel_present = IntegerField('How many meetings with applicants do you wish to have?')

    #applicant_properties = NoValidationSelectMultipleField('Skills applicant should excel at')

class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=1, max=25)]
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
    email = TextField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
