from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
import enum

from models import *

def subject_query():
    return Subject.query

class TutorForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    email = StringField(
        'email', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired()]
    )
    # image_link = StringField(
    #     'image_link'
    # )
    classes = QuerySelectMultipleField('Subjects', validators=[DataRequired()],
                                        query_factory=subject_query)

class SubjectForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    grade = SelectField(
        'Grade', validators=[DataRequired()],
        coerce=int, choices=[
            ('7', '7'),
            ('8', '8'),
            ('9', '9'),
            ('10', '10'),
            ('11', '11'),
            ('12', '12')
        ])