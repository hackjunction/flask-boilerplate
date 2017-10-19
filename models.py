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
    excellent_skills = db.Column(db.Text())
    extra_skills = db.Column(db.Text())
    titles = db.Column(db.Text())
    amount_meetings = db.Column(db.Integer())

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
