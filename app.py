import os
from flask import Flask, request, redirect, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import db_drop_and_create_all, setup_db, Tutor
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
setup_db(app)
CORS(app)

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
  return render_template('templates/forms/new_tutor.html', form=form)

@app.route('/tutors/create, methods=['POST'])
def add_tutor():
  tutor_form = TutorForm(request.form)
  # body = request.get_json()
  #  CHECK bc API uses JSON... vs form?? 
  name = body.get('name', None)
  phone = body.get('phone', None)
  email = body.get('email', None)
  subjects = form.subjects.raw_data
  # WHAT IS RAW_DATA 

  try:
    form = TutorForm()
    name = form.name.data

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/subjects/create', methods=['GET'])
def create_subject_form():
  form = SubjectForm()
  return render_template('templates/forms/new_subject.html', form=form)

@app.route('/subjects/create, methods=['POST'])
def add_subject():
  boday = request.get_json
  tutor_form = TutorForm(request.form)
  # body = request.get_json()
  #  CHECK bc API uses JSON... vs form?? 
  name = body.get('name', None)
  phone = body.get('phone', None)
  email = body.get('email', None)
  subjects = form.subjects.raw_data
  # WHAT IS RAW_DATA 

  try:
    form = TutorForm()
    name = form.name.data

if __name__ == '__main__':
    app.run(debug=True)
