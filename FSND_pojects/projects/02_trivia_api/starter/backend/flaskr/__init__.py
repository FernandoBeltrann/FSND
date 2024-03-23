import os
import json
from flask import Flask, Response,request, abort, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import select
import random

from sqlalchemy import func

from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [book.format() for book in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  migrate = Migrate(app,db)
  CORS(app, resources={r"/*": {"origins": "*"}})
  app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV')
  app.config['FLASK_APP'] = os.environ.get('FLASK_APP')
  app.config['FLASK_DEBUG'] = os.environ.get('FLASK_DEBUG')

  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs

  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  
  @app.route('/categories', methods = ['GET'])
  def get_categories():
      categories = Category.query.all()

      categories = [category.format() for category in categories]

      response_json = json.dumps({

          'success': True,
          'categories': categories
          #'total_questions': len(categories)
            
      }, indent=2)  # Sets the indentation level to 2 spaces
      print(response_json)
      return Response(response_json, mimetype='application/json')
  

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
'''

  @app.route('/questions', methods = ['GET'])
  def get_questions():
      page = request.args.get('page', 1, type=int)

      questions = Question.query.all()
      categories = Category.query.all()

      categories = [category.subject for category in categories]
      
      current_questions = paginate_questions(request, questions)

      if len(current_questions) == 0:
            abort(404)


      response_json = json.dumps({

          'success': True,
          'questions': current_questions,
          'total_questions': len(questions),
          'categories': categories
          #'current_category': questions.category
            
      }, indent=2)  # Sets the indentation level to 2 spaces
      return Response(response_json, mimetype='application/json')

  '''


  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:id>', methods = ['DELETE'])
  def delete_question(id):
        
      question = Question.query.filter_by(id=id).one()
      question.delete()

      current_questions = Question.query.all()
      current_questions = [format(question) for question in current_questions]

      categories = Category.query.all()
      categories = [format(category) for category in categories]


      response_json = json.dumps({

        'success': True,
        'questions': current_questions,
        'total_questions': len(current_questions),
        'categories': categories
        #'current_category': questions.category
            
      }, indent=2)  # Sets the indentation level to 2 spaces
      return Response(response_json, mimetype='application/json')

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    data = request.get_json()  # This gets the JSON data sent in the request body
    question = data['question']
    answer = data['answer']
    difficulty = data['difficulty']
    category = data['category']

    new_question = Question(question=question, answer=answer, difficulty=difficulty, category=category-1)
    new_question.insert()

    response_json = json.dumps({

        'success': True
            
      }, indent=2)  # Sets the indentation level to 2 spaces
    return Response(response_json, mimetype='application/json')



  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_question():
    data = request.get_json()  # This gets the JSON data sent in the request body
    searchTerm = data['searchTerm']
    print('Search Term:', searchTerm)

    questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
    print('Questions Found:', questions)  # Debug print
    #categories = Category.query.filter(Category.id in (questions.category))

    # Assuming Category.id is an Integer
    category_ids = [q.category for q in questions]  # This assumes that `category` is storing the category ID
    categories = Category.query.filter(Category.id.in_(category_ids)).all()


    questions = [question.format() for question in questions ]
    categories = [category.format() for category in categories ]


    response_json = json.dumps({

        'questions': questions,
        'totalQuestions': len(questions),
        'currentCategory':categories,
        'success': True
            
      }, indent=2)  # Sets the indentation level to 2 spaces
    return Response(response_json, mimetype='application/json')


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_q_for_category(id):

    questions = Question.query.filter(Question.category == id).all()

    category_ids = [q.category for q in questions]  # This assumes that `category` is storing the category ID
    categories = Category.query.filter(Category.id.in_(category_ids)).all()

    questions = [question.format() for question in questions]
    categories = [category.format() for category in categories]

    response_json = json.dumps({

        'questions': questions,
        'totalQuestions': len(questions),
        'currentCategory':categories,
        'success': True
            
      }, indent=2)  # Sets the indentation level to 2 spaces
    return Response(response_json, mimetype='application/json') 
     

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_questions_for_quiz():
    data = request.get_json()
    previous_questions = data['previous_questions']
    quiz_category = data['quiz_category']

    try:
        # Assume quiz_category is an object with 'id' key, and you want to compare with category ID
        category_id = int(quiz_category['id']) if quiz_category['id'] > 0 else None
        
        # Filter questions based on the category (if specified) and that are not in previous_questions
        if category_id:
            new_question_query = Question.query.filter(Question.category == category_id, ~Question.id.in_(previous_questions))
        else:
            new_question_query = Question.query.filter(~Question.id.in_(previous_questions))
        
        new_question = new_question_query.order_by(func.random()).first()

        if new_question:
            formatted_question = new_question.format()
        else:
            formatted_question = None

        response_json = json.dumps({
            'question': formatted_question,
            'success': True
        }, indent=2)
        return Response(response_json, mimetype='application/json')
    except Exception as e:
        # Handle the exception in an appropriate way, such as logging it and returning an error response
        response_json = json.dumps({
            'success': False,
            'error': str(e)
        }, indent=2)
        return Response(response_json, mimetype='application/json', status=500)



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def error404(error):
    response_json = json.dumps({
            'success': False,
            'error': 'Resource not found'
            })
    return Response(response_json, mimetype='application/json', status=404)


  @app.errorhandler(422)
  def error422(error):
     response_json = json.dumps({
            'success': False,
            'error': 'Unprocesable Resource'
            })
     return Response(response_json, mimetype='application/json', status=422)
  
  return app

    