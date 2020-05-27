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

# ----------- TUTORS ----------
# CREATE 

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
            tutor = Tutor(
                name=new_name, phone=new_phone,
                email=new_email, classes=new_classes
            )
            tutor.insert()

        except Exception as e:
            print('ERROR: ', str(e))
            abort(422)

        flash(f'Tutor:{new_name} successfully created!')

        return jsonify({
            'success': True,
            'tutors': tutor.format()
        })

    # EDIT
    @app.route('/tutors/<int:id>/edit', methods=['GET'])
    # @login_required
    # @requires_auth('patch:tutors')
    def edit_tutor(*args, **kwargs):
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

        return render_template('/forms/edit_tutor.html', title='Edit Tutor', form=form)



    @app.route('/tutors/<int:id>edit', methods=['PATCH'])
    # @requires_auth('patch:tutors')
    def edit_tutor_submit(*args, **kwargs):
        id = kwargs['id']
        form = TutorForm()
        tutor = Tutor.query.filter_by(id=id).one_or_none()

        if tutor is None:
            abort(404)

        body = request.get_json()

        if 'name' in body:
            tutor.name = form.name.data
        if 'phone' in body:
            tutor.phone = form.phone.data
        if 'email' in body:
            tutor.email = form.email.data
        if 'classes' in body:
            tutor.classes = form.classes.data

        try:
            tutor.insert()
        except Exception as e:
            print('EXCEPTION: ', str(e))
            abort(400)

        flash(f'{tutor.name}\'s details successfully updated.')

        return jsonify({
            'success': True,
            'tutors': tutor.format()
        })



# DELETE


# ----------- SUBJECTS ----------
# CREATE 

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

# EDIT


# DELETE


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