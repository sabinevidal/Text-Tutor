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
def index():
    return render_template('index.html')


@app.route('/tutors')
def get_tutors():
  tutors = tutor.query.all()

  if len(tutors) == 0:
    abort(404)

  return jsonify({
    'success': True,
    'tutors': tutors
  })

@app.route('/tutors/new', methods=['POST'])
def add_tutor():
  body = request.get_json()


if __name__ == '__main__':
    app.run(debug=True)