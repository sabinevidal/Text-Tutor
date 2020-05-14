# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

'''
Tutor
'''

class Tutor(db.Model):
    __tablename__ = 'Tutors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    availability = Column(Boolean, nullable=True)

    grades = relationship('Grade', backref='tutor', lazy=True)
    subjects = relationship('Subject', backref='tutor', lazy=True)

# TODO: what is this???
    # def __init__(self, )

'''
Grade
'''
class Grade(db.Model):
    __tablename__ = 'Grades'

    id = Column(Integer, primary_key=True)
    name = Column(Integer, nullable=False)
    tutor_id =  Column(Integer, ForeignKey('Tutor.id'), primary_key=True)

'''
Subject
'''
class Subject(db.Model):
    __tablename__ = 'Subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tutor_id =  Column(Integer, ForeignKey('Tutor.id'), primary_key=True)