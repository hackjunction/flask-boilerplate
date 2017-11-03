#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import logging
from logging import Formatter, FileHandler
from forms import *
from functools import wraps
import os
import json

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Gotta import this only after setting up the app
import models

skills = ['AngularJS', 'Assembly', 'Bash', 'C', 'C#', 'C++', 'Clojure',
           'CoffeeScript', 'CSS', 'Excel', 'Go', 'Groovy', 'Haskell', 'HTML',
           'Java', 'JavaScript', 'Kotlin', 'Lua', 'Matlab', 'Node.js',
           'Objective-C', 'Perl', 'PHP', 'PowerPoint', 'Python', 'Qt', 'R', 'React',
           'Ruby', 'Scala', 'SQL', 'Swift', 'TypeScript', 'VBA', 'VB.NET',
           'Visual Basic 6', '.NET Core', 'Other']

jobtitles = ['Frontend Developer', 'Backend Developer', 'Full-Stack Developer',
             'Manager / Executive', 'Mobile Developer', 'Data Scientist',
             'Entrepreneur', 'Analyst', 'Machine Learning Developer', 'Industrial Designer',
             'Web Design', 'Product Design', 'Other design related', 'Server Specialist',
             'IT', 'Hardware Engineer']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = u""
bcrypt = Bcrypt(app)

# Login manager user loade
@login_manager.user_loader
def load_user(user_id):
    user = models.User.query.filter_by(id=user_id).first()
    return user

# Automatically tear down SQLAlchemy.

@app.teardown_request
def shutdown_session(exception=None):
    print 'Tearing down SQLAlchemy'
    db.session.commit()
    db.session.flush()
    db.session.remove()


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))
            
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    errors = []
    success = False
    form = CompanyForm(request.form)
    if request.method == 'POST':
        if form.validate():
            # Company data
            time_present = form.time_present.data
            company_name = form.name.data
            amount_meetings = form.amount_meetings.data
            company_strengths = form.company_strengths.data
            personnel_present = form.personnel_present.data
            contact_email = form.contact_email.data

            applicants = []
            # Applicant data
            for applicant in form.applicants:
                job_nature = applicant.job_nature.data
                experience_in_years = applicant.experience_in_years.data
                extra_skills = json.dumps(applicant.extra_skills.data)
                skills_description = applicant.skills_description.data
                job_description = applicant.job_description.data
                excellent_skills = json.dumps(applicant.excellent_skills.data)

                new_applicant = models.Applicant(job_nature, experience_in_years, excellent_skills, 
                                                extra_skills, skills_description, job_description)

                applicants.append(new_applicant)

            try:
                db.session.commit()
                success = True
            except Exception, e:
                print 'Commit failed'
                db.session.rollback()
                print str(e)
                errors.append('Database commit failure.')
            if (success):
                current_user.amount_meetings = amount_meetings
                current_user.personnel_present = personnel_present
                current_user.time_present = time_present
                current_user.company_name = company_name
                current_user.contact_email = contact_email
                current_user.company_strengths = company_strengths
                current_user.applicants = applicants

                try:
                    db.session.commit()
                    success = True
                except Exception, e:
                    print 'Commit failed'
                    db.session.rollback()
                    print str(e)
                    errors.append('Database commit failure.')


        else:
            print 'Form did not validate:'
            flash_errors(form)

    else:
        if (current_user.company_name is not None):
            # If company name is set, all other data should also already be there
            form.name.data = current_user.company_name
            form.contact_email.data = current_user.contact_email
            form.amount_meetings.data = current_user.amount_meetings
            form.personnel_present.data = current_user.personnel_present
            form.company_strengths.data = current_user.company_strengths
            form.time_present.data = current_user.time_present

            i = 0
            for applicant in current_user.applicants:
                form.applicants[i].job_nature.data = applicant.job_nature
                form.applicants[i].experience_in_years.data = applicant.experience_in_years
                form.applicants[i].excellent_skills.data = json.loads(applicant.excellent_skills)
                form.applicants[i].extra_skills.data = json.loads(applicant.extra_skills)
                form.applicants[i].skills_description.data = applicant.skills_description
                form.applicants[i].job_description.data = applicant.job_description
                i = i + 1

        else:
            # Set a couple of default values if user has never submitted form
            form.name.data = current_user.name
            form.contact_email.data = current_user.email

    form.applicants[0].excellent_skills.choices = [(g, g) for g in skills]
    form.applicants[0].extra_skills.choices = [(g, g) for g in skills]

    form.applicants[1].excellent_skills.choices = [(g, g) for g in skills]
    form.applicants[1].extra_skills.choices = [(g, g) for g in skills]


    return render_template('pages/home.html', form=form, errors=errors,
                           skills=skills, success=success)


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    errors = []
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = models.User.query.filter_by(email=email).first()
        if not user:
            errors.append('Invalid login')
            return render_template('forms/login.html', form=form, errors=errors)

        elif not bcrypt.check_password_hash(user.password, password):
            errors.append('Invalid login')

        else:
            login_user(user)
            return redirect(url_for('home'))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print err

    return render_template('forms/login.html', form=form, errors = errors)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    errors = []
    if request.method == 'POST' and form.validate():
        username = form.name.data
        password = form.password.data
        email = form.email.data

        user = db.session.query(models.User).filter_by(email=email).first()
        if user:
            errors.append('User with this email already exists.')

        user = db.session.query(models.User).filter_by(name=username).first()
        if user:
            errors.append('User with this company name already exists.')

        print user

        if not user:
            hashed_pass = bcrypt.generate_password_hash(password)
            try:
                user = models.User(username, hashed_pass, email)
                if user:
                        db.session.add(user)
                        db.session.commit()
                        login_user(user)
                        return redirect(url_for('home'))
                else:
                    errors.append('Invalid reg')
            except:
                errors.append('User already exists')


    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print err

    return render_template('forms/register.html', form=form, errors=errors)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


# Error handlers.

'''
@app.errorhandler(500)
def internal_error(error):
    db_session.rollback()
    return render_template('errors/500.html'), 500
'''

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
