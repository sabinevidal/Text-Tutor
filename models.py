# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
import json
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

database_filename = "text-tutor.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

'''
Tutor
'''

class Tutor(db.Model):
    __tablename__ = 'tutor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    availability = Column(Boolean, nullable=True)

    tutor_subjects = relationship('Subject', backref='tutor', lazy=True)

    # TODO: what is this???
    # def __init__(self, )
    def __repr__(self):
        return '<Tutor %r>' % self.name

    def short(self):
        return {
            'id': self.id,
            'name': self.name
        }
    

'''
Subject
'''
class Subject(db.Model):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    grade =  Column(Integer, nullable=False)
'''
Tutor Subject TODO: Do i need this?????
'''

class TutorsSubjects(db.Model):
    __tablename__ = 'tutors_subjects'

    tutor_id = db.Column(Integer, ForeignKey('Tutors.id'), primary_key=True)
    subject = db.Column(Integer, ForeignKey('Subjects.id'), primary_key=True)

