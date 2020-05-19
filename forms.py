from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL
import enum


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