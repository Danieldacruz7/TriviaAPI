import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_NAME, DB_USER, DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_NAME
        self.database_path = "postgres://{}:{}@{}/{}".format(DB_USER, 
                                                             DB_USER,
                                                             'localhost:5432',
                                                             self.database_name)
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

    def test_category_retrieval(self):
        res = self.client().get('/categories')
        data  = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)
    
    def test_category_retrieval_404_error(self):
        res = self.client().get('/categories/1')
        data  = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        
    def test_paginated_question_retrieval(self):
        res = self.client().get('/questions')
        data  = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)
    
    def test_paginated_question_retrieval_error(self):
        res = self.client().get('/questions=page?10')
        data  = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        
    def test_question_insertion(self):
        new_question = {
                        'question': 'The question?',
                        'answer': 'The answer.',
                        'difficulty': 1,
                        'category': 1
                       }
        prev_number_of_questions = len(Question.query.all())
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        total_questions = len(Question.query.all())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_questions, prev_number_of_questions + 1)
        
    def test_question_insertion_422_error(self):
        new_question = {
                        'question': 'The question?',
                        'answer': 'The answer.',
                        'difficulty': 1,
                        'category': 10 # Wrong category
                       }
        prev_number_of_questions = len(Question.query.all())
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        total_questions = len(Question.query.all())
        self.assertEqual(res.status_code, 422)
    
    def test_question_deletion(self):
        new_question = {
                        'question': 'The question?',
                        'answer': 'The answer.',
                        'difficulty': 1,
                        'category': 1
                       }
        res = self.client().post('/questions', json=new_question)
        question_to_delete = Question.query.filter(Question.question == new_question['question']).first()
        question_id = question_to_delete.id
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_deleting_nonexistent_question_404_error(self):
        res = self.client().delete('/questions/a')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_question_search(self):
        search = {"searchTerm": "title", "quiz_category": "All"}
        res = self.client().post('/questions/search', json=search)
        data  = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_question_search_error(self):
        search = {"searchTerm":"title", "quiz_category":"All"}
        res = self.client().post('/questions/searche', json=search)
        data  = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        
    def test_question_categories(self):
        res = self.client().get('/categories/1/questions')
        data  = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_question_categories_404_error(self):
        res = self.client().get('/categories/8/questions')
        self.assertEqual(res.status_code, 404)
    
    def test_play_game(self):
        game = {"quiz_category": {"type": "Science", "id": 1}, "previous_questions": []}
        res = self.client().post('/quizzes', json=game)
        data  = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_play_game_404_error(self):
        game = {"category": "Wrong", "previous_questions": []}
        res = self.client().post('/quizzes', json=game)
        self.assertEqual(res.status_code, 404)
    
    
        
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    