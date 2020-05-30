import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import *
from models import *

# PRIVATE USER GENERATED FOR TESTING PURPOSES ONLY
# HAS ALL PERMISSIONS:
# "get:tutors", "get:subjects",
# "post:tutor", "post:subject", "patch:tutor", "delete:tutor"
PRIVATE_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhlbkxVTVBwNkFQR3FFNGVKeDVOaiJ9.eyJpc3MiOiJodHRwczovL2Rldi1mYXY1ZHA0ZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5OGI4YzIwZmI2YzYwYzgzYTQxZGJmIiwiYXVkIjoicnVubmVycyIsImlhdCI6MTU4NzIyODAyNSwiZXhwIjoxNTg3MzE0NDI1LCJhenAiOiJVQ0hrank2RlJDb2lLU1R5bWpJQUtrTVFHckVvUjl1YyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnN0YXQiLCJnZXQ6YWxsX2F0aGxldGVzIiwiZ2V0OmFsbF9zdGF0cyIsInBhdGNoOnN0YXQiLCJwb3N0OmF0aGxldGUiLCJwb3N0OnN0YXQiXX0.cWdbRVe2khLIKwQSDyrJ3wRlnPkr93eh9LMHxahTnd8DVCP2RnS4A5oJL37erYFK14BLfuKYdpmLnSLanR6yhTqlT0bzMObhEV45NmhaAZ2aAF7HA3cfdcNJ1TRIwIGd7KabP0Qi3_SFKHClDu-FFFWH1XFTiB81I4BCeSIs0zpnpXirYjuZY2maW2J8siO0tvWZUqWnJ0psUtt9B7hP39KGayVFiWFYCmgwcszWAkHUPqNZKWJAGj3YtytcxDpIR2xnQ7Q0H89Hs2yskeY-zKJNGdUxxmbLIR0BQ3FH-5c8NvAa70Cu891jhglTvyGPekNj3M11Y6q_mcz35rvmcw'

# PUBLIC USER GENERATED FOR TESTING PURPOSED ONLY
# HAS NO PERMISSIONS
PUBLIC_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhlbkxVTVBwNkFQR3FFNGVKeDVOaiJ9.eyJpc3MiOiJodHRwczovL2Rldi1mYXY1ZHA0ZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5OWNkYjg5NjA3MTEwYzllY2U3ZDNjIiwiYXVkIjoicnVubmVycyIsImlhdCI6MTU4NzIyODA4MiwiZXhwIjoxNTg3MzE0NDgyLCJhenAiOiJVQ0hrank2RlJDb2lLU1R5bWpJQUtrTVFHckVvUjl1YyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOltdfQ.UMyFC77QER9CcZYr3HtruNHnSJUw7ps496sa1fjHpqtpLdxB00gpUjuM-42dJeYUldrpMU30OVeqSqGQr48MdsX_qsN7wZoAM80QbT_zTf2PwCtQ2B_NhqcSMXvX76HX8FsCQATr5AkpSi9-DmRdHuPtJwdIJ9Qt03FY69Kp5rCrTGsevdJIleM8pmEemHa8sKnI6JyOsS0OOwRY234q7lBwCM_u72_UwQib5sDyYB3tfLY5n87-dv5O85KXRZl7_JSJtgiPS5hSt-Lm_9Ta7Xhl5rP4rm6Afjsc47mQQAb5WpD5XmyDdsqEnRLQ_E1UHREZQv5IE2yHXXYimGG8MA'


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
        self.headers_private = {
            'Content-Type': 'application/json',
            'Authorization': PRIVATE_TOKEN}
        self.headers_public = {
            'Content-Type': 'application/json',
            'Authorization': PUBLIC_TOKEN}


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # creates test plant
    def test_get_tutors(self):
        """ Tests success of loading tutors"""
        response = self.client().get('/api/tutors',
                headers=self.headers_public)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_subjects(self):
        """Tests success of loading tutors"""
        response = self.client().get('/api/subjects',
                headers=self.headers_public)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_tutors(self):
        """Tests tutor creation"""
        test_tutor = {
            'id': 654321,
            'name': 'Test',
            'phone': '123456789',
            'email': 'test@email.com'
            # 'classes': 'classes' TODO
        }
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        response = self.client().post('/api/tutors',
                data=json.dumps(test_tutor),
                headers=self.headers_private)
        data = json.loads(response.data)

        # check status code, success message & compare length before & after
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 654321)

    def test_create_subjects(self):
        """Tests tutor creation"""
        test_subject = {
            'id': 765432,
            'name': 'English',
            'grade': '14',
        }

        response = self.client().post('/api/subjects',
                data=json.dumps(test_subject),
                headers=self.headers_private)
        data = json.loads(response.data)

        # check status code, success message & compare length before & after
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['grade'], 14)

    def test_edit_tutor(self):
        """Tests PATCH tutor """
        patched_tutor = {
            'email': 'patch@email.com'
        }

        response = self.client().patch(
                '/api/tutors/654321',
                json=patched_tutor,
                headers=self.headers_private)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['tutor']['email'], 'patch@email.com')

    def test_edit_subject(self):
        """Tests PATCH subject """
        patched_subject = {
            'grade': 15
        }

        response = self.client().patch(
                '/api/subjects/765432',
                json=patched_subject,
                headers=self.headers_private)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['subject']['grade'], 15)


    def test_delete_tutor(self):
        """ Tests question delete success """
        delete_tutor = Tutor(
            name="Lizzo",
            phone='1231234123',
            email="lizzo@email.com",
            classes=" "
        )
        delete_tutor.insert()
        t_id = delete_tutor.id

        response = self.client().delete('/api/tutors/{}'.format(t_id),
                headers=self.headers_private)
        data = json.loads(response.data)

        # check status code, success message & compare length before & after
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], t_id)

    def test_delete_subject(self):
        """Tests question delete success """
        delete_subject = Subject(
            name="Art",
            grade='8'
        )

        delete_subject.insert()
        s_id = subject.id


        response = self.client().delete('/api/subject/{}'.format(s_id),
                headers=self.headers_private)
        data = json.loads(response.data)

        # check status code, success message & compare length before & after
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], s_id)

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

    def test_422_edit_tutor(self):
        """test failure of patch tutor error 422"""
        patched_tutor = {
            'email': 12345
        }

        response = self.client().patch(
                '/api/tutors/654321',
                json=patched_tutor,
                headers=self.headers_private)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])

     def test_422_edit_subject(self):
        """test failure of patch subject error 422"""
        patched_subject = {
            'grade': 'grade'
        }

        response = self.client().patch(
                '/api/subjects/765432',
                json=patched_subject,
                headers=self.headers_private)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])

    def test_get_subject_tutors(self):
        """test success of getting tutors by subjects"""
        response = self.client().get('/api/subjects/1/tutors',
                headers=self.headers_public)
        data = json.loads(response.data)

        # check status code, success message,
        # num of questions and current category
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['tutors']))
        self.assertTrue(data['total_tutors'])

    def test_404_get_subject_tutors(self):
        """test for 404 error of getting tutors by subjects"""
        response = self.client().get('/api/subjects/1/tutors',
                headers=self.headers_public)
        data = json.loads(response.data)

        # check status code, false success message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
