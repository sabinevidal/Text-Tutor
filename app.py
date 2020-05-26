import os
import json
from flask import Flask, request, redirect, abort, jsonify, render_template, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_wtf import Form
from wtforms import Form
import wtforms_json

from models import *
from forms import *
from sqlalchemy.dialects.postgresql import JSON
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS with '*' for origins
    CORS(app, resources={'/': {'origins': '*'}})

    # CORS headers to set access control
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    @TODO uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    # db_drop_and_create_all()

# ----------------------------------
# ROUTES
# ----------------------------------

    @app.route('/')
    @app.route('/index')
    def index():
        user = {'username': 'Sabine'}
        posts = [
            {
                'tutor': {'name': 'John'},
                'subjects': 'Gr8 Maths'
            },
            {
                'tutor': {'name': 'Susan'},
                'subjects': 'Gr9 Science, gr10 Maths'
            }
        ]
        return render_template('index.html', title='Home!', user=user, posts=posts)


    @app.route('/tutors')
    def get_tutors():
        tutors = Tutor.query.all()

        if len(tutors) == 0:
            abort(404)

        return jsonify({
        'success': True,
        'tutors': tutors
        })

    @app.route('/tutors/create', methods=['GET'])
    def create_tutor_form():
        form = TutorForm()
        return render_template('/forms/new_tutor.html', title='New Tutor', form=form)

    @app.route('/tutors/create', methods=['POST'])
    def add_tutor():
        body = request.get_json()
        form = TutorForm(request.form)

        new_name = form.name.data
        new_phone = form.phone.data
        new_email = form.email.data
        new_classes = form.classes.data

        try:
            new_tutor = Tutor(
                name=new_name, phone=new_phone,
                email=new_email, classes=new_classes
            )
            new_tutor.insert()

        except Exception as e:
            print('ERROR: ', str(e))
            abort(422)

        flash(f'Tutor:{new_name} successfully created!')

        return jsonify({
            'success': True,
            'subject': new_tutor.format()
        })


    @app.route('/subjects/create', methods=['GET'])
    def create_subject_form():
        form = SubjectForm()
        return render_template('/forms/new_subject.html', title='New Subject', form=form)

    @app.route('/subjects/create', methods=['POST'])
    def add_subject():
        body = request.get_json()
        form = SubjectForm(request.form)

        new_name = form.name.data
        new_grade = form.grade.data

        try:
            new_subject = Subject(
                name=new_name, grade=new_grade
            )
            new_subject.insert()

        except Exception as e:
            print('ERROR: ', str(e))
            abort(422)

        flash(f'{new_grade}:{new_name} successfully created!')

        return jsonify({
            'success': True,
            'subject': new_subject.format()
        })

    return app

app = create_app()

if __name__ == '__main__':
    app.run()