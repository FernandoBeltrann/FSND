import json
import os
from flask import Flask, Response, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # -Get all books with pagination-
    #
    # @TODO: Write a route that retrivies all books, paginated.
    #         You can use the constant above to paginate by eight books.
    #         If you decide to change the number of books per page,
    #         update the frontend to handle additional books in the styling and pagination
    #         Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, the webpage will display books including title, author, and rating shown as stars

    @app.route('/books', methods = ['GET'])
    def get_books():
        books = Book.query.all()

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * BOOKS_PER_SHELF
        end = start + BOOKS_PER_SHELF
        formatted_books = [book.format() for book in books]
        response_json = json.dumps({

            'books': formatted_books[start:end],
            'total_books': len(formatted_books),
            'success': True,
            
        }, indent=2)  # Sets the indentation level to 2 spaces
        return Response(response_json, mimetype='application/json')



    # -Update rating of a book-
    #
    # @TODO: Write a route that will update a single book's rating.
    #         It should only be able to update the rating, not the entire representation
    #         and should follow API design principles regarding method and route.
    #         Response body keys: 'success'
    # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh

    @app.route('/books/<int:id>', methods = ['PATCH'])
    def update_rating(id):

        data = request.get_json()
        rating = data.get('rating')
        result = Book.query.filter(Book.id == id).update({"rating": rating})

        response_json = json.dumps({
            'success': True
        })  

        if result:
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Book not found"), 404


    # @TODO: Write a route that will delete a single book.
    #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'

    # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.
        
    @app.route('/books/<int:id>', methods = ['DELETE'])
    def delete_book(id):

        book = Book.query.get(id)
        book.delete()

        books = Book.query.all()
        formatted_books = [book.format() for book in books]



        try:
            book.delete()
            
            formatted_books = [book.format() for book in books]
            books = Book.query.all()
            response_json = json.dumps({

                'success': True,
                'deleted': id,
                'books': formatted_books,
                'total_books': len(books)

            })  

            return response_json
        
        except Exception as e:

            response_json = json.dumps({

                'success': False,
                'books': formatted_books,
                'total_books': len(books),
                'error': str(e)

            })
            
            return response_json


    # @TODO: Write a route that create a new book.
    #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    # TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books.
    #       Your new book should show up immediately after you submit it at the end of the page.
        
    @app.route('/books', methods = ['POST'])
    def add_book():

        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        rating = data.get('rating')

        new_book = Book(title=title, author=author, rating=rating)
        id = new_book.id
        new_book.insert()
        
        books = Book.query.all()
        formatted_books = [book.format() for book in books]

        response_json = json.dumps({

            'success': True,
            'created': id,
            'books': formatted_books,
            'total_books': len(books)
        })  

        if new_book:
            return response_json
        else:
            return jsonify(success=False, error="Book not created"), 404

    return app
