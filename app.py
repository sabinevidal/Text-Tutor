import os
import json
from flask import Flask, request, redirect, abort, jsonify, render_template
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
    wtforms_json.init()

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
        tutor_form = TutorForm(request.form)
        # body = request.get_json()
        #  CHECK bc API uses JSON... vs form??
        name = body.get('name', None)
        phone = body.get('phone', None)
        email = body.get('email', None)
        image_link = body.get('image_link', None)
        gr_subjects = form.gr_subjects.raw_data
        # WHAT IS RAW_DATA

        try:
            form = TutorForm()
            name = form.name.data
            phone = form.phone.data
            email = form.email.data
            image_link = form.image_link.data
            # subjects =
        except Exception as e:
            print('ERROR: ', str(e))
            abort(422)


    @app.route('/subjects/create', methods=['GET'])
    def create_subject_form():
        form = SubjectForm()
        return render_template('/forms/new_subject.html', title='New Subject', form=form)

    @app.route('/subjects/create', methods=['POST'])
    def add_subject():
        body = request.get_json()
        form = TutorForm(request.form)

        name = request.json.get('name')
        grade = request.json.get('grade')

        if ((name == "") or (grade == "")):
            abort(422)

        subject = Subject(
            name=name, grade=grade
        )

        try:
            subject.insert()
        except Exception as e:
            print('ERROR: ', str(e))
            abort(422)

        flash(f'Plant {name} successfully created!')

        return jsonify({
            'success': True,
            'subject': subject.format()
        })

    return app