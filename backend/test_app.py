import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import *
from models import *


class TextTutorTestCase(unittest.TestCase):
    """This class represents the text tutor test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "text_tutor_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # creates test plant
    def create_test_tutor(self):

        # create and insert new plant
        tutor = Tutor(name=self.test_tutor['name'],
                      phone=self.test_tutor['phone'],
                      email=self.test_tutor['email'],
                      classes=self.test_tutor['classes'])
        tutor.insert()

        return tutor.id

    def create_test_subject(self):

        # create and insert new plant
        subject = Subject(name=self.test_subject['name'],
                      grade=self.test_subject['grade'])
        subject.insert()

        return subject.id

    def test_get_tutors(self):
        """ Tests success of loading tutors"""
        response = self.client().get('/api/tutors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_subjects(self):
        """Tests success of loading tutors"""
        response = self.client().get('/api/subjects')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_tutors(self):
        """Tests tutor creation"""
        tutor = self.create_test_tutor

        tutors_before = len(Tutor.query.all())

        response = self.client().post('/api/tutors', json=tutor)
        data = json.loads(response.data)
        tutors_after = len(Tutor.query.all())

        # check status code, success message & compare length before & after
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(tutors_after, tutors_before + 1)

    def test_create_subjects(self):
        """Tests tutor creation"""
        subject = {
            'name': 'English',
            'grade': '7',
        }

        subjects_before = len(Subject.query.all())

        response = self.client().post('/api/subjects', json=subject)
        data = json.loads(response.data)
        subjects_after = len(Subject.query.all())

        # check status code, success message & compare length before & after
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(subjects_after, subjects_before + 1)

    def test_edit_tutor(self):
        """Tests PATCH tutor """
        t_id = self.create_test_subject(self)

        # set json data
        request_data = {
            'name': 'PATCH TEST',
            'email': None,
            'phone': None,
            'classes': None
        }

        # get response with updated name json and load data
        response = self.client().patch('/api/tutors/{}'.format(t_id),
                                       json=request_data)
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['tutor']['name'], 'PATCH TEST')

    def test_edit_subject(self):
        """Tests PATCH subject """
        s_id = self.create_test_subject(self)

        # set json data
        request_data = {
            'name': 'PATCH TEST',
            'grade': None
        }

        # get response with updated name json and load data
        response = self.client().patch('/api/subjects/{}'
                                        .format(s_id),
                                        json=request_data)
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['subject']['name'], 'PATCH TEST')


    def test_delete_tutor(self):
        """ Tests question delete success """
        tutor = Tutor(
            name="Lizzo",
            phone='1231234123',
            email="lizzo@email.com",
            classes=" "
        )

        tutor.insert()
        t_id = tutor.id

        tutors_before = Tutor.query.all()

        response = self.client().delete('/api/tutors/{}'.format(t_id))
        data = json.loads(response.data)

        tutors_after = Tutor.query.all()
        tutor = Tutor.query.filter(Tutor.id == 1).one_or_none()

        # check status code, success message & compare length before & after
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], t_id)
        self.assertTrue(len(tutors_before) - len(tutors_after) == 1)
        self.assertEqual(tutor, None)

    def test_delete_subject(self):
        """Tests question delete success """
        subject = Subject(
            name="Art",
            grade='8'
        )

        subject.insert()
        s_id = subject.id

        subjects_before = Subject.query.all()

        response = self.client().delete('/api/subject/{}'.format(s_id))
        data = json.loads(response.data)

        subjects_after = Subject.query.all()
        subject = Subject.query.filter(Subject.id == 1).one_or_none()

        # check status code, success message & compare length before & after
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], s_id)
        self.assertTrue(len(subjects_before) - len(subjects_after) == 1)
        self.assertEqual(subject, None)

    def test_422_create_tutor(self):
        """test failure of question creation error 400"""
        tutors_before = Tutor.query.all()

        response = self.client().post('/api/tutors', json={})
        data = json.loads(response.data)
        tutors_after = Tutor.query.all()

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(tutors_before) == len(tutors_after))

    def test_422_create_subject(self):
        """test failure of question creation error 400"""
        subjects_before = Subject.query.all()

        response = self.client().post('/api/subjects', json={})
        data = json.loads(response.data)
        subjects_after = Subject.query.all()

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(subjects_before) == len(subjects_after))

    def test_get_subject_tutors(self):
        """test success of getting tutors by subjects"""
        response = self.client().get('/api/subjects/1/tutors')
        data = json.loads(response.data)

        # check status code, success message,
        # num of questions and current category
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['tutors']))
        self.assertTrue(data['total_tutors'])

    def test_404_get_subject_tutors(self):
        """test for 404 error of getting tutors by subjects"""
        response = self.client().get('/api/subjects/1/tutors')
        data = json.loads(response.data)

        # check status code, false success message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
