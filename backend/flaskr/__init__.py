import os

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    #CORS(app, resources={r"*/api/*" : {"origins": '*'}})
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, PUT, POST, PATCH, DELETE, OPTION"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        """
        Queries the Category table within the database for 
        all possible categories. Converts the results into a
        dictionary for serialization using Jsonify.   

        Args:
            None

        Returns:
            JSON object.

        Test for API: curl http://localhost:5000/categories
        """
        
        categories = Category.query.all()
        
        categories_dict = {}
        for i in categories:
            categories_dict[i.id] = i.type
            
        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": categories_dict,
                "total_questions": len(Category.query.all()),
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        """
        Queries the Questions table within the database for 
        all possible questions. The query results are then 
        paginated for the 10 questions based on the page 
        selected. Converts the results into a dictionary 
        for serialization using Jsonify.   

        Args:
            None

        Returns:
            JSON object.
        
        Test: curl http://localhost:5000/questions?pages=1
        """
        
        questions = Question.query.join(Category, Category.id == Question.category).all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.order_by('id').all()
        
        list_of_questions = []
        list_of_categories = {}
        for i in categories:
            list_of_categories[i.id] = i.type
                
        if len(questions) == 0:
            abort(404)
        
        return jsonify(
            {
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(questions),
            "categories": list_of_categories,
            'currentCategory': list_of_categories[current_questions[-1]['category']]
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """
        Deletes a question based on its ID. 
        
        Test: curl -X DELETE http://localhost:5000/questions/5
        """
        # 
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            new_dict = {}
            new_dict['id'] = question.id
            new_dict['question'] = question.question

            Question.delete(question)

            return jsonify(
                {
                    "success": True,
                    "delete": question.id
                }
            )

        except:
            abort(422)
         

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        """
        Adds a new question to the database. 
        
        Test: curl -d '{"category": 1, "difficulty":1, "question":"The question?", "answer":"The answer."}' -H 'Content-Type: application/json' http://localhost:5000/questions
        """
        try:
            body = request.get_json()
            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            category = body.get("category", None)
            difficulty_score = body.get("difficulty", None)

            question = Question(question=new_question, answer=new_answer, category=category, difficulty=difficulty_score)
            Question.insert(question)
            question_dict = {}
            question_dict['question'] = new_question
            question_dict['answer'] = new_answer
            question_dict['category'] = category
            question_dict['difficulty_score'] = difficulty_score

            return jsonify(
                    {
                        "success": True,
                        "question": question_dict
                    }
                )
        except:
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        """
        Returns questions that have partial string matching with the search term. 
        
        Test: curl -d '{"searchTerm":"title", "quiz_category":"All"}' -H 'Content-Type: application/json' http://localhost:5000/questions/search
        """
        body = request.get_json()
        search_term = str(body.get('searchTerm', None))
        current_category = body.get('quiz_category', None)
        try: 
            questions = Question.query.join(Category, Category.id == Question.category).filter(Question.question.like('%' + search_term + '%')).all()
            current_questions = paginate_questions(request, questions)

            return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'totalQuestions': len(questions),
                    'currentCategory': current_category,
                    })
        
        except:
            abort(404)
                                                                                           
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def get_question_categories(category_id):
        """
        Returns questions based on its category. 
        
        Test: curl http://localhost:5000/categories/1/questions
        """
        questions = Question.query.join(Category, Category.id == Question.category).filter(Category.id == category_id).all()
        current_category = Category.query.filter(Category.id == category_id).one_or_none()
        
        data = []
        for i in questions:
            new_dict = {}
            new_dict['id'] = i.id
            new_dict['question'] = i.question
            new_dict['answer'] = i.answer
            new_dict['difficulty'] = i.difficulty
            new_dict['category'] = i.category
            
            data.append(new_dict)
            
        if len(questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": data,
                "totalQuestions": len(questions),
                "currentCategory": current_category.type
            })
    

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_game():
        """
        Starts a quiz that randomly selects question based on category or altogether. 
        
        Test: curl -d '{"quiz_category": {"type": "Science", "id": 1}, "previous_questions":[]}' -H 'Content-Type: application/json' http://localhost:5000/quizzes
        """
        body = request.get_json()
        previous_questions_id = body.get("previous_questions", [])
        current_category = body.get("quiz_category")
        
        try: 
            if current_category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.join(Category, Category.id == Question.category).filter(Category.type == current_category['type']).all()
            length_of_list = len(questions)

            questions_dict = {}
            list_of_categories = []
            list_of_questions = []

            for i in questions:
                if i.id in previous_questions_id:
                    continue
                else:
                    question_to_ask = {}
                    question_to_ask['id'] = i.id
                    question_to_ask['question'] = i.question
                    question_to_ask['answer'] = i.answer
                    question_to_ask['difficulty'] = i.difficulty
                    question_to_ask['category'] = i.category
                    list_of_questions.append(question_to_ask)


            if len(list_of_questions) != 0:
                question = random.choice(list_of_questions)

                return jsonify({
                                "success": True,
                                'question': question
                            })
            else:
                return jsonify({
                                "success": False
                            })

        except:
            abort(404)
        

    """"
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    return app
