from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
import enum

from models import Tutor, Subject

def subject_query():
    return Subject.query

class TutorForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    email = StringField(
        'email', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired()]
    )
    subjects = QuerySelectMultipleField('Subjects', validators=[DataRequired()],
                                        query_factory=subject_query, allow_blank=True, get_label='subjects')
