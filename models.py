# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import relationship, backref
import json

from config import Config
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
    app.config.from_object(Config)
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

#format tutor's subjects
def format_gr_subjects(subjects):
    return [subject.format() for subject in subjects]

# Tutor
class Tutor(db.Model):
    __tablename__ = 'tutors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    image_link = Column(String, nullable=False)

    subject = relationship('Subject', secondary="tutor_subjects", backref=backref('tutors', lazy=True))

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'subject': self.subject
        }

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return '<Tutor: %r>' %self.name

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': format_subjects(self.subject)
        }

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    grade =  Column(Integer, nullable=False)

    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __repr__(self):
        return '<Subject: %r>' %self.name

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'grade': self.grade
        }


class TutorsSubjects(db.Model):
    __tablename__ = 'tutor_subjects'

    tutor_id = Column(Integer, ForeignKey('tutors.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)

    tutor = relationship(Tutor, backref=backref("tutor_subjects", cascade="all, delete-orphan"))
    subject = relationship(Subject, backref=backref("tutor_subjects", cascade="all, delete-orphan"))

