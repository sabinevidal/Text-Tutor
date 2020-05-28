from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, AnyOf, URL, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
import enum

from models import *

def subject_query():
    return Subject.query

class TutorForm(FlaskForm):
    name = StringField(
        'Name', [DataRequired()]
    )
    email = StringField(
        'Email', [DataRequired()]
    )
    phone = StringField(
        'Phone', [DataRequired()]
    )
    # image_link = StringField(
    #     'image_link'
    # )
    classes = QuerySelectMultipleField('Subjects', [DataRequired()],
                                        query_factory=subject_query)
    submit = SubmitField('Submit')

class SubjectForm(FlaskForm):
    name = StringField(
        'Name', [DataRequired()]
    )
    grade = SelectField(
        'Grade', [DataRequired()],
        coerce=int, choices=[
            ('7', '7'),
            ('8', '8'),
            ('9', '9'),
            ('10', '10'),
            ('11', '11'),
            ('12', '12')
        ])
    submit = SubmitField('Submit')