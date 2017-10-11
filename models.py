from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app import db

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.
class User(Base):
    __tablename__ = 'Users'

    # Basic fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

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



# Create tables.
Base.metadata.create_all(bind=engine)
