from sqlalchemy import Column, Integer, String
from app import db

# Set your classes here.
class User(db.Model):
    __tablename__ = 'Users'

    # Basic fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    company_name = db.Column(db.String(120), unique=True)
    contact_email = db.Column(db.String(120), unique=False)

    # Desired applicant data
    amount_meetings = db.Column(db.Integer())
    personnel_present = db.Column(db.Integer())
    time_present = db.Column(db.String(100))
    company_strengths = db.Column(db.String(1000))

    applicants = db.relationship('Applicant', backref='company', lazy=True)

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)  # python 2


class Applicant(db.Model):
    __tablename__ = 'Applicants'
    id = db.Column(db.Integer, primary_key=True)

    job_nature = db.Column(db.String(50))
    experience_in_years = db.Column(db.String(50))
    excellent_skills = db.Column(db.Text())
    extra_skills = db.Column(db.Text())
    skills_description = db.Column(db.String(1000))
    job_description = db.Column(db.String(1000))

    company_id = db.Column(db.Integer, db.ForeignKey('Users.id'),
        nullable=True)

    def get_id(self):
        return unicode(self.id)  # python 2


    def __init__(self, job_nature, experience_in_years, excellent_skills, extra_skills, skills_description, job_description):
        self.job_nature = job_nature
        self.experience_in_years = experience_in_years
        self.excellent_skills = excellent_skills
        self.extra_skills = extra_skills
        self.skills_description = skills_description
        self.job_description = job_description