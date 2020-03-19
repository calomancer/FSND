import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}@{}/{}".format('postgres:606285', 'localhost:5432', self.database_name)
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
    Done
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_paginate_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_beyond_valid_paginate_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_get_questions_in_category(self):
        category_id=1
        res = self.client().get('/categories/'+str(category_id)+'/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        
    def test_404_beyond_questions_in_category(self):
        category_id=1000
        res = self.client().get('/categories/'+str(category_id)+'/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_post_questions(self):
        test_json = {"question":"How good is this?", "answer":"So Good", "difficulty":"1", "category":"5"}
        res = self.client().post('/questions', json=test_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions']) 

    def test_post_Incorrect_questions(self):
        test_json = {"question":"", "answer":"So Good", "difficulty":"1", "category":"5"}
        res = self.client().post('/questions', json=test_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        
    def test_delete_question(self):
        question_id = Question.query.first()
        res = self.client().delete('/questions/' + str(question_id.id))
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertTrue(data['deleted'])
        self.assertEquals(str(data['deleted']), str(question_id.id))

    def test_delete_out_of_range_question(self):
        question_id = 1000
        res = self.client().delete('/questions/' + str(question_id))
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_search(self):
        searchTerm = {"searchTerm": "Tom"}
        res = self.client().post('/search', json=searchTerm)
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['currentCategory'], None)

    def test_search_unknown_term(self):
        searchTerm = "tom"
        res = self.client().post('/search', json=searchTerm)
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 422)
        self.assertEquals(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_quizzes(self):
        category = {"quiz_category":{"id":4,"type":"History"},"previous_questions": []}
        res = self.client().post('/quizzes', json=category)
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_quizzes_not_existing_category(self):
        category = {"quiz_category":{"id":500,"type":"History"},"previous_questions": []}
        res = self.client().post('/quizzes', json=category)
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()