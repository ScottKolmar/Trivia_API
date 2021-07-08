import json
import os
from re import A
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.orm import joinedload_all
from sqlalchemy.sql.expression import except_all

from werkzeug.exceptions import SecurityError

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS
    cors = CORS(app, resources={
        r"localhost:5000/*": {
            "origins": "*"
        }
    })

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Set up paginate function
    def paginate(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_selection = questions[start:end]

        return current_selection

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():

        # Get categories
        selection = Category.query.order_by(Category.id).all()
        categories = {}
        for category in selection:
          categories[category.id] = category.type

        return jsonify({
            "success": True,
            "categories": categories
        })

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():

        # Get questions
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate(request, selection)

        # Get all categories
        categories = Category.query.order_by(Category.id).all()
        category_return = {}
        for category in categories:
          category_return[category.id] = category.type

        return jsonify({
            "success": True,
            "questions": current_questions,
            "totalQuestions": len(current_questions),
            "currentCategory": None,
            "categories": category_return
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:

            # Abort if question isn't in db
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            # Delete question
            question.delete()

            return jsonify({
                "success": True,
                "deleted": question_id
            })

        except BaseException:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():

        # Get search term
        body = request.get_json()
        search = body.get('searchTerm')

        try:

            if search:

                # Search questions
                selection = Question.query.filter(
                    Question.question.ilike('%{}%'.format(search)))
                current_questions = paginate(request, selection)

                return jsonify({
                    "success": True,
                    "questions": current_questions,
                    "totalQuestions": len(current_questions)
                })

            else:

                # Get question contents
                question = body.get('question', None)
                answer = body.get('answer', None)
                category = body.get('category', None)
                difficulty = body.get('difficulty', None)

                # Abort if None in any field
                if question is None or answer is None or category is None or difficulty is None:
                    abort(422)

                # Add question to db
                new_question = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty)
                new_question.insert()

                return jsonify({
                    "success": True,
                    "created": new_question.id
                })

        except BaseException:
            abort(422)

    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def retrieve_category_questions(category_id):

        # Get category and abort if it isn't available
        current_category = Category.query.filter(
            Category.id == category_id).one_or_none()
        if current_category is None:
            abort(404)

        # Get questions in category
        selection = Question.query.filter(
            Question.category == category_id).all()
        current_questions = paginate(request, selection)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "totalQuestions": len(current_questions),
            "currentCategory": current_category.type
        })

    @app.route('/quizzes', methods=['POST'])
    def create_quiz():

        # Get input data
        body = request.get_json()
        category = body.get('quiz_category')
        previous_question_ids = body.get('previous_questions')

        # Abort if no category provided
        if category is None:
            abort(422)

        # Abort if category not in db
        category_in_db = Category.query.filter(
            Category.id == category["id"]).one_or_none()
        if category_in_db is None:
            abort(422)

        # Post if category is in db
        else:

            selection = Question.query.filter(
                Question.category == category["id"]).all()
            selection_filtered = [
                question for question in selection if question not in previous_question_ids]
            questions = paginate(request, selection_filtered)
            next_question = random.choice(questions)

        return jsonify({
            "success": True,
            "question": next_question
        })

    @app.route('/categories', methods=['POST'])
    def create_category():

        # Get category input
        body = request.get_json()
        cat_type = body.get("type")

        # Abort if no category input provided
        if cat_type is None:
            abort(422)

        # Try to post category
        try:
            category = Category(type=cat_type)
            category.insert()

            return jsonify({
                "success": True,
                "created": category.id
            })

        except BaseException:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Request"
        }), 422

    return app
