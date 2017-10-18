#!/bin/bash
export DEBUG=True
export SECRET_KEY=verysecret
export DATABASE_URL=sqlite:///database.db

source venv/bin/activate
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
