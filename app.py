import os
import json
from flask import Flask, request, redirect, abort, jsonify, render_template, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import Form

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

        return render_template('index.html', title='Home', tutors=tutors, subjects=subjects)

# ----------- TUTORS ----------

    @app.route('/tutors')
    def get_tutors():
        '''
        Handles GET requests for getting all tutors
        '''
        response = get_tutors_api()
        data = json.loads(response.data)
        tutors = data['tutors']

        return render_template('pages/tutors.html', tutors=tutors), 200

    @app.route('/tutors/<int:id>')
    def show_tutor(id):
        '''
        Handles GET requests for getting tutor by id
        '''

        response = show_tutor_api(id)
        data = json.loads(response.data)
        tutor = data['tutor']

        return render_template('/pages/show_tutor.html', tutor=tutor), 200

    @app.route('/tutors/create', methods=['GET'])
    # @login_required
    # @requires_auth('post:tutors')
    def create_tutor_form():
        '''
        Handles GET requests for new tutor form page.
        '''
        form = TutorForm()
        return render_template('/forms/new_tutor.html', title='New Tutor', form=form),200

    # EDIT
    @app.route('/tutors/<int:id>/edit', methods=['GET'])
    # @login_required
    # @requires_auth('patch:tutors')
    def edit_tutor(*args, **kwargs):
        '''
        Handles GET requests for edit tutor form.
        '''
        id = kwargs['id']
        form = TutorForm()
        tutor = Tutor.query.filter_by(id=id).one_or_none()

        tutor={
            "id": tutor.id,
            "name": tutor.name,
            "phone": tutor.phone,
            "email": tutor.email,
            "classes": tutor.classes
        }
        # form placeholders
        form.name.process_data(tutor['name'])
        form.phone.process_data(tutor['phone'])
        form.email.process_data(tutor['email'])
        form.classes.process_data(tutor['classes'])

        return render_template('/forms/edit_tutor.html', title='Edit Tutor', form=form), 200

# ----------- SUBJECTS ----------

    @app.route('/subjects')
    def get_subjects():
        '''
        Handles GET requests for getting all subjects.
        '''
        response = get_subjects_api()
        data = json.loads(response.data)
        subjects = data['subjects']

        return render_template('/pages/subjects.html', subjects=subjects), 200

    @app.route('/subjects/create', methods=['GET'])
    # @login_required
    # @requires_auth('post:subject')
    def create_subject_form():
        '''
        Handles GET requests for new subject form page.
        '''
        form = SubjectForm()
        return render_template('/forms/new_subject.html', title='New Subject', form=form), 200

    @app.route('/subjects/<int:id>/edit')
    # @login_required
    # @requires_auth('patch:subjects')
    def edit_subject(*args, **kwargs):
        '''
        Handles GET requests for edit subject form.
        '''
        id = kwargs['id']
        form = SubjectForm()
        subject = Subject.query.filter_by(id=id).one_or_none()

        tutor={
            "id": subject.id,
            "name": subject.name,
            "grade": subject.grade
        }
        # form placeholders
        form.grade.process_data(subject['grade'])
        form.name.process_data(subject['name'])

        return render_template('/forms/edit_subject.html', title='Edit Subject', form=form), 200

    # -----------------------------------------------------------
    # API Routes
    # -----------------------------------------------------------

    @app.route('/api/tutors')
    def get_tutors_api():
        '''
        Handles API GET requests for getting all tutors. Returns JSON.
        '''
        tutors = Tutor.query.all()

        if len(tutors) == 0:
            abort(404)

        tutors = format_tutors(tutors)

        return jsonify({
            'success': True,
            'tutors': tutors
        })

    @app.route('/api/tutors/<int:id>')
    def show_tutor_api(id):
        '''
        Handles API GET requests for getting tutor by ID. Returns JSON.
        '''
        tutor = Tutor.query.filter_by(id=id).one_or_none()

        if tutor is None:
            abort(404)

        return jsonify({
            'success': True,
            'tutor': tutor.format()
        })
    
    @app.route('/api/tutors/create', methods=['POST'])
    # @requires_auth('post:tutors')
    def create_tutor_api():

        body = request.get_json()
        form = TutorForm(request.form)

        new_name = form.name.data
        new_phone = form.phone.data
        new_email = form.email.data
        new_classes = form.classes.data

        tutor = Tutor(
                name=new_name, phone=new_phone,
                email=new_email, classes=new_classes
        )

        try:
            tutor.insert()

        except Exception as e:
            print('ERROR: ', str(e))
            abort(422)

        flash(f'Tutor:{new_name} successfully created!')

        return jsonify({
            'success': True,
            'tutors': tutor.format()
        })

    @app.route('/api/tutors/<int:id>/edit', methods=['PATCH'])
    # @requires_auth('edit:tutors')
    def edit_tutor_api(*args, **kwargs):
        '''
        Handles API PATCH requests for tutors.
        '''
        id = kwargs['id']
        form = TutorForm()
        tutor = Tutor.query.filter_by(id=id).one_or_none()

        if tutor is None:
            abort(404)
        try:
            body = request.get_json()

            if 'name' in body:
                tutor.name = form.name.data
            if 'phone' in body:
                tutor.phone = form.phone.data
            if 'email' in body:
                tutor.email = form.email.data
            if 'classes' in body:
                tutor.classes = form.classes.data


            tutor.insert()
        except Exception as e:
            print('EXCEPTION: ', str(e))
            abort(400)

        flash(f'{tutor.name}\'s details successfully updated.')

        return jsonify({
            'success': True,
            'tutors': tutor.format()
        })

    @app.route('/api/tutors/<int:id>', methods=['DELETE'])
    # @requires_auth('delete:tutors')
    def delete_tutor_api(*args, **kwargs):
        '''
        Handles API DELETE requests for tutors.
        '''
        id = kwargs['id']

        tutor = Tutor.query.filter_by(id=id).one_or_none()

        if drink is None:
            abort(404)

        try:
            tutor.delete()
        except Exception as e:
            print('EXCEPTION: ', str(e))
            abort(422)

        flash(f'{tutor.name}\'s details successfully deleted.')

        return jsonify({
            'success': True,
            'tutor': tutor.name,
            'tutor_id': id
        })

    @app.route('/api/subjects')
    def get_subjects_api():
        '''
        Handles API GET requests for getting all subjects. Returns JSON.
        '''
        subjects = SUbject.query.all()

        if len(subjects) == 0:
            abort(404)

        subjects = format_subjects(subjects)

        return jsonify({
            'success': True,
            'subjects': subjects
        })

    @app.route('/api/subjects/<int:id>')
    def show_subject_api(id):
        '''
        Handles API GET requests for getting subjects by id. Returns JSON.
        '''
        subject = Subject.query.filter_by(id=id).one_or_none()

        if subject is None:
            abort(404)

        return jsonify({
            'succes': True,
            'subject': subject.format()
        })

    @app.route('/api/subjects/create', methods=['POST'])
    # @requires_auth('post:subjects')
    def create_subject_api()
        '''
        Handles API POST requests for creating new subject. Returns JSON.
        '''
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

        flash(f'{subject.new_grade}:{subject.new_name} successfully created!')

        return jsonify({
            'success': True,
            'subject': new_subject.format()
        })

    @app.route('/api/subjects/<int:id>/edit', methods=['PATCH'])
    # @requires_auth('patch:subjects')
    def edit_subject_api(*args, **kwargs):
        '''
        Handles API PATCH requests for subjects.
        '''
        id = kwargs['id']
        form = SubjectForm()
        subject = Subject.query.filter_by(id=id).one_or_none()

        if subject is None:
            abort(404)
        try:
            body = request.get_json()

            if 'name' in body:
                subject.name = form.name.data
            if 'grade' in body:
                subject.grade = form.grade.data


            subject.insert()
        except Exception as e:
            print('EXCEPTION: ', str(e))
            abort(400)

        flash(f'{subject.grade}:{subject.name} successfully updated.')

        return jsonify({
            'success': True,
            'subject': subject.format()
        })

    @app.route('/api/subjects/<int:id>', methods=['DELETE'])
    # @requires_auth('delete:subjects')
    def delete_subject_api(*args, **kwargs):
        '''
        Handles API DELETE requests for subjects.
        '''
        id = kwargs['id']

        subject = Subject.query.filter_by(id=id).one_or_none()

        if subject is None:
            abort(404)

        try:
            subject.delete()
        except Exception as e:
            print('EXCEPTION: ', str(e))
            abort(422)

        flash(f'{subject.grade}:{subject.name} successfully deleted.')

        return jsonify({
            'success': True,
            'grade': subject.grade,
            'subject': subject.name,
            'subject_id': id
        })

    @app.route('/api/key')
    def get_api_key():
        '''
        Endpoint for getting API key for curl requests and testing
        '''

        return render_template('/pages/api_key.html')




# -----------------------------------------------------------
# Error Handlers
# -----------------------------------------------------------

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 422

    return app




app = create_app()

if __name__ == '__main__':
    app.run()