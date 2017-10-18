#!/bin/bash
export DEBUG=True
export SECRET_KEY=verysecret
export DATABASE_URL=sqlite:///database.db

source venv/bin/activate
python app.py
