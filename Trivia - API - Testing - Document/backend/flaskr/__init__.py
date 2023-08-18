from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Question, Category
import random

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', default=1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def list_to_dict(datas):
    result = {}
    for data in datas:
        result[data.id] = data.type

    return result


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_all_categoies():
        categories = Category.query.order_by(Category.id).all()
        if len(categories) == 0:
            abort(404)

        # adding all categories to the dict
        result = list_to_dict(categories)

        return jsonify({
            'success': True,
            'categories': result,
        })

    @app.route('/questions', methods=['GET'])
    def get_questions_and_pagination():
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        pagination = paginate_questions(request, questions)

        if len(questions) == 0 or len(pagination) == 0:
            abort(404)

        try:
            dict_categories = list_to_dict(categories)

            return jsonify({
                'questions': pagination,
                'totalQuestions': len(questions),
                'categories': dict_categories,
                'currentCategory': 'History'
            })
        except Exception:
            abort(400)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question_by_id(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(400)

            return jsonify({
                'success': True,
            })
        except Exception:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        question = body.get('question')
        answer = body.get('answer')
        difficulty = body.get('difficulty')
        category = body.get('category')

        try:
            question = Question(question=question, answer=answer, category=category,
                                difficulty=difficulty)
            question.insert()
            return jsonify({
                'success': True,
            })
        except Exception:
            abort(422)

    @app.route('/search', methods=['POST'])
    def search_questions():
        searchTerm = request.get_json().get('searchTerm')
        questions = Question.query.filter(
            Question.question.ilike('%' + searchTerm + '%'))
        if questions is None:
            results = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'questions': results,
                'totalQuestions': len(questions)
            })
        else:
            abort(404)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category_id(category_id):
        try:
            category = Category.query.filter_by(id=category_id).one_or_none()
            if category:
                questions = Question.query.filter(
                    Question.category == category_id).all()
                results = paginate_questions(request, questions)
                return jsonify({
                    'success': True,
                    'questions': results,
                    'totalQuestions': len(questions)
                })
            else:
                abort(404)
        except:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        body = request.get_json()
        previousQuestion = body.get('previous_questions')
        quizCategory = body.get('quiz_category')

        try:
            category_id = quizCategory['id']
            if category_id == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                    category=category_id).all()

            randomIndex = random.randint(0, len(questions)-1)
            nextQuestion = questions[randomIndex]

            while nextQuestion.id not in previousQuestion:
                nextQuestion = questions[randomIndex]
                return jsonify({
                    'success': True,
                    'question': nextQuestion.format(),
                    'previousQuestion': previousQuestion
                })
        except:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "internal server error"
        }), 500

    return app
