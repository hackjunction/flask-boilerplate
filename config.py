import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = os.environ['DEBUG']

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = os.environ['SECRET_KEY']

# Connect to the database
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
