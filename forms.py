from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectMultipleField, IntegerField, TextAreaField, RadioField, FieldList, FormField
from wtforms.validators import DataRequired, EqualTo, Length

# Multiselect field without validation
class NoValidationSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        """per_validation is disabled"""
        return True

# Radio button field without validation
class NoValidationRadioField(RadioField):
    def pre_validate(self, form):
        """per_validation is disabled"""
        return True

class ApplicantForm(Form):
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        Form.__init__(self, *args, **kwargs)
    excellent_skills = NoValidationSelectMultipleField('Skills applicant should excel at')
    extra_skills = NoValidationSelectMultipleField('Skills applicant should excel at')
    skills_description = TextAreaField('Skills description')
    experience_in_years = NoValidationRadioField('Experience',
        choices=[('value_one','1'),('value_two','1-2 years'),('value_three','3-5 years'),('value_four','5+ years')])
    job_description = TextAreaField('Job Description')
    job_nature = NoValidationRadioField('Job nature?',
        choices=[('value_one','Full time'),('value_two','Part Time'),('value_three','Both')])


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

    amount_meetings = IntegerField('Amount of meetings')
    personnel_present = IntegerField('Amount of persons')
    company_strengths = TextAreaField('Company Stregths', validators=[DataRequired(), Length(min=6, max=200)])  
    applicants = FieldList(FormField(ApplicantForm), min_entries=2)


  

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
