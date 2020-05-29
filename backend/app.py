import os
import json
from flask import Flask, request, redirect, abort, jsonify, render_template, flash, session, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import *
from sqlalchemy.dialects.postgresql import JSON
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS with '*' for origins
    CORS(app, resources={'/': {'origins': '*'}}, supports_credentials=True)

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

# TODO: index home page
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

    @app.route('/api/tutors')
    def get_tutors():
        '''
        Handles GET requests for tutors.
        '''
        tutors = Tutor.query.all()

        if len(tutors) == 0:
            abort(404)

        response = {
            'success': True,
            'tutors': tutors
        }
        return jsonify(response)

    @app.route('/api/tutors/<int:id>')
    def show_tutor(id):
        '''
        Handles GET requests for tutor by id.
        '''
        tutor = Tutor.query.filter_by(id=id).one_or_none()

        if tutor is None:
            abort(404)

        response = {
            'success': True,
            'tutor': tutor.format()
        }
        return jsonify(response)


# CREATE
    @app.route('/api/tutors', methods=['POST'])
    def add_tutor():
        '''
        Handles POST requests for creating a tutor.
        '''
        body = request.get_json()

        new_name = body.get('name')
        new_phone = body.get('phone')
        new_email = body.get('email')
        new_classes = body.get('classes')

        # try:
        tutor = Tutor(
            name=new_name, phone=new_phone,
            email=new_email, classes=new_classes
        )
        print('tutor: ', tutor)
        tutor.insert()

        # except Exception as e:
        #     print('ERROR: ', str(e))
        #     abort(422)

        # flash(f'Tutor:{new_name} successfully created!')

        response = {
            'success': True,
            'tutor': tutor.format()
        }

        return jsonify(response)

    # EDIT
    # @app.route('/api/tutors/<int:id>', methods=['GET'])
    # # @login_required
    # # @requires_auth('patch:tutors')
    # def edit_tutor(*args, **kwargs):
    #     id = kwargs['id']
    #     tutor = Tutor.query.filter_by(id=id).one_or_none()

    #     tutor={
    #         "id": tutor.id,
    #         "name": tutor.name,
    #         "phone": tutor.phone,
    #         "email": tutor.email,
    #         "classes": tutor.classes
    #     }
    #     # form placeholders
    #     # form.name.process_data(tutor['name'])
    #     # form.phone.process_data(tutor['phone'])
    #     # form.email.process_data(tutor['email'])
    #     # form.classes.process_data(tutor['classes'])

    #     response = {
    #         'success': True,
    #         'tutor': tutor.format()
    #     }

    #     return jsonify(response)



    @app.route('/api/tutors/<int:id>', methods=['PATCH'])
    # @requires_auth('patch:tutors')
    def edit_tutor(*args, **kwargs):
        id = kwargs['id']

        tutor = Tutor.query.filter_by(id=id).one_or_none()

        if tutor is None:
            abort(404)

        body = request.get_json()

        if 'name' in body:
            tutor.name = body['name']
        if 'phone' in body:
            tutor.phone = body['phone']
        if 'email' in body:
            tutor.email = body['email']
        if 'classes' in body:
            tutor.classes = body['classes']

        try:
            tutor.insert()
        except Exception as e:
            print('EXCEPTION: ', str(e))
            abort(400)

        # flash(f'{tutor.name}\'s details successfully updated.')

        response = {
            'success': True,
            'tutors': tutor.format()
        }

        return jsonify(response)



# DELETE
    @app.route('/api/tutors/<int:id>', methods=['DELETE'])
    # @requires_auth('delete:tutors')
    def delete_tutor(*args, **kwargs):
        '''
        Handles API DELETE requests for tutors.
        '''
        id = kwargs['id']

        tutor = Tutor.query.filter_by(id=id).one_or_none()

        if tutor is None:
            abort(404)

        try:
            tutor.delete()
        except Exception as e:
            print('EXCEPTION: ', str(e))
            abort(422)

        # flash(f'{tutor.name}\'s details successfully deleted.')

        return jsonify({
            'success': True,
            'tutor': tutor.name,
            'tutor_id': id
        })


# ----------- SUBJECTS ----------
# CREATE

    @app.route('/api/subjects', methods=['POST'])
    def add_subject():
        body = request.get_json()
        print('body: ', body)

        name = body.get('name')
        grade = body.get('grade')

        try:
            subject = Subject(
                name=name, grade=grade
            )
            subject.insert()

        except Exception as e:
            print('ERROR: ', str(e))
            abort(422)

        response = {
            'success': True,
            'subject': subject.format()
        }

        return jsonify(response)


    @app.route('/api/subjects')
    def get_subjects():
        subjects = Subject.query.order_by(Subject.grade).all()

        if len(subjects) == 0:
            abort(404)

        subjects = format_subjects(subjects)

        response = {
            'success': True,
            'subjects': subjects
        }
        return jsonify(response)


    @app.route('/api/subjects/<int:id>')
    def show_subject(id):
        '''
        Handles GET requests for getting subjects by id
        '''
        subject = Subject.query.filter_by(id=id).one_or_none()

        if subject is None:
            abort(404)

        response = {
            'success': True,
            'subject': subject.format()
        }
        return jsonify(response)

# EDIT
  @app.route('/api/subjects/<int:id>', methods=['PATCH'])
    # @requires_auth('patch:tutors')
    def edit_subject(*args, **kwargs):
        '''
        Handles PATCH requests for subjects.
        '''
        id = kwargs['id']

        subject = Subject.query.filter_by(id=id).one_or_none()

        if subject is None:
            abort(404)

        body = request.get_json()

        if 'name' in body:
            subject.name = body['name']
        if 'grade' in body:
            subject.grade = body['grade']

        try:
            subject.insert()
        except Exception as e:
            print('EXCEPTION: ', str(e))
            abort(400)

        # flash(f'{subject.name}\'s details successfully updated.')

        response = {
            'success': True,
            'subjects': subject.format()
        }

        return jsonify(response)



# DELETE
    @app.route('/api/subjects/<int:id>', methods=['DELETE'])
    # @requires_auth('delete:tutors')
    def delete_subject(*args, **kwargs):
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

        # flash(f'{subject.name}\'s details successfully deleted.')

        return jsonify({
            'success': True,
            'subject': subject.name,
            'subject_id': id
        })

    @app.route('/api/subjects/<int:id>/tutors')
    def get_subject_tutors(id):
        '''
        Handles GET requests for getting tutors based on subjects
        '''
        subject = Subject.query.filter_by(id=id).one_or_none()

        try:
            selection = Tutor.query.filter_by(subject=subject.id).all()

            return jsonify({
                'success': True,
                'tutors': selection,
                'total_tutors': len(Tutor.query.all()),
            })
        except:
            abort(400)




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