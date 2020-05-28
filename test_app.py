import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Question, Category, db


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

    def test_get_tutors(self):
        """ Tests success of loading tutors"""
        response = self.client().get('/tutors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_tutors(self):
        """Tests tutor creation"""
        tutor = {
            'name': 'Lizzo',
            'phone': '1231234123',
            'email': 'lizzo@email.com',
        }

        # get questions before post. Create question, load response data
        # and get num questions after
        questions_before = len(Question.query.all())

        response = self.client().post('/questions', json=tutor)
        data = json.loads(response.data)
        questions_after = len(Question.query.all())

        # check status code, success message & compare length before & after
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(questions_after, questions_before + 1)

    def test_delete_question(self):
        """ Tests question delete success """
        # create a new question to be deleted
        question = Question(question="is a test?",
                            answer='yes', category=1, difficulty=1)
        question.insert()
        q_id = question.id

        questions_before = Question.query.all()

        response = self.client().delete('/questions/{}'.format(q_id))
        data = json.loads(response.data)

        questions_after = Question.query.all()
        question = Question.query.filter(Question.id == 1).one_or_none()

        # check status code, success message & compare length before & after
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], q_id)
        self.assertTrue(len(questions_before) - len(questions_after) == 1)
        self.assertEqual(question, None)

    def test_422_create_question(self):
        """test failure of question creation error 400"""
        # get num of questions before post, create question without json data,
        # get num questions after
        questions_before = Question.query.all()

        response = self.client().post('/questions', json={})
        data = json.loads(response.data)
        questions_after = Question.query.all()

        # check status code, false success message
        # and compare length before & after
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(questions_before) == len(questions_after))

    def test_search_question(self):
        """test success fo searchin questions"""
        # send post request with search term, load response data
        # new_search = {'searchTerm': 'a'}
        response = self.client().post('/questions/search', json={
            'searchTerm': 'palace'})
        data = json.loads(response.data)

        # check status code, success message,
        # that there are questions in the search results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_404_search_questions(self):
        """test for no search results 404"""
        response = self.client().post('/questions/search', json={
            'searchTerm': ''})
        data = json.loads(response.data)

        # check status code, false success message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_get_category_questions(self):
        """test success of getting questions by categories"""
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        # check status code, success message,
        # num of questions and current category
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_get_category_questions(self):
        """test for 404 error with no questions from category"""
        response = self.client().get('/categories/a/questions')
        data = json.loads(response.data)

        # check status code, false success message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_quiz(self):
        """test success of playing quiz"""
        quiz_round = {'previous_questions': [], 'quiz_category': {
            'type': 'Geography', 'id': 15}}
        response = self.client().post('/quizzes', json=quiz_round)
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_get_quiz(self):
        """test 422 error if quiz game fails"""
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        # check status code, false success message
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
