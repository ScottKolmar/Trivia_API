import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv

load_dotenv(dotenv_path=r'C:\Users\skolmar\Udacity\Trivia\FSND\projects\02_trivia_api\starter\credentials.env')

user_name = os.environ.get('USER')
password = os.environ.get('PASSWORD')


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            user_name, password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_retrieve_categories(self):

        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

        return

    def test_retrieve_paginated_questions(self):

        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

        return

    def test_retrieve_category_questions(self):

        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        return

    def test_404_sent_requesting_bad_category(self):
        res = self.client().get('/categories/10000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found")

        return

    def test_delete_question(self):

        res = self.client().delete('/questions/11')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 11)

        return

    def test_422_when_delete_bad_question(self):

        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Request')

        return

    def test_create_question(self):

        new_question = {
            'question': "What's up doc?",
            'answer': "Silly Wabbit",
            'category': 2,
            'difficulty': 5
        }

        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

        return

    def test_create_question_with_no_inputs(self):
        new_question = {
            'question': None,
            'answer': None,
            'category': None,
            'difficulty': None
        }

        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Request")

        return

    def test_get_questions_with_good_search(self):

        res = self.client().post('/questions', json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

        return

    def test_get_questions_with_bad_search(self):

        res = self.client().post('/questions',json={"searchTerm": "Brumblecrumps"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['totalQuestions'], 0)

        return

    def test_create_quiz(self):
        quiz_query = {
            "quiz_category": {
                "type": "Entertainment",
                "id": "5"
                },
            "previous_questions": [1, 6]
        }
        res = self.client().post('/quizzes', json=quiz_query)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        return

    def test_422_if_bad_quiz_category(self):
        quiz_query = {
            "quiz_category": {
                "type": "Elves",
                "id": "69"
                },
            "previous_questions": [1, 2]
        }
        res = self.client().post('/quizzes', json=quiz_query)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Request")

        return

    def test_create_category(self):
        category_input = {
            "type": "Lord of the Rings"
        }

        res = self.client().post('/categories', json=category_input)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

        return

    def test_create_category_with_no_type(self):
        category_input = {
            "type": None
        }

        res = self.client().post('/categories', json=category_input)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Request")

        return


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
