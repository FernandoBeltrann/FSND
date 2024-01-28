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


def paginate_books(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF

    books = [book.format() for book in selection]
    current_books = books[start:end]

    return current_books

def create_app(db_URI="", test_config=None):
    # create and configure the app
    app = Flask(__name__)
    if db_URI:
        print('Using NON-default Database')
        setup_db(app, db_URI)
    else:
        print('Using Default Database')
        setup_db(app)
    
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
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

        current_books = paginate_books(request, books)

        if len(current_books) == 0:
            abort(404)


        response_json = json.dumps({

            'success': True,
            'books': current_books,
            'total_books': len(books)
            
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

        try:
            result = Book.query.filter(Book.id == id).one_or_none()
            if result is None:
                abort(404)

            result.rating = int(rating)
            result.update()
        
            response_json = json.dumps({

                'success': True,
                'id': id
                
            }, indent=2)  # Sets the indentation level to 2 spaces
            return Response(response_json, mimetype='application/json')


        except:
            #return jsonify(success=False, error="Book not found"), 404
            # return jsonify({
            #     'success': False
            # }),404 

            response_json = json.dumps({

                    'success': False,
                    
            }, indent=2),404  # Sets the indentation level to 2 spaces
            return Response(response_json, mimetype='application/json')
                


    # @TODO: Write a route that will delete a single book.
    #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'

    # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.
        
    # @app.route('/books/<int:id>', methods = ['DELETE'])
    # def delete_book(id):

    #     try:
    #         book = Book.query.get(id)
    #         book.delete()
            
    #         books = Book.query.all()
    #         formatted_books = [book.format() for book in books]
    #         response_json = json.dumps({

    #             'books': formatted_books,
    #             'success': True,
    #             'deleted_id': id,
    #             'total_books': len(books)

    #         }, indent=2)
    #         return response_json
        
    #     except Exception as e:

    #         books = Book.query.all()
    #         formatted_books = [book.format() for book in books]

    #         response_json = json.dumps({

    #             'success': False,
    #             'books': formatted_books,
    #             'total_books': len(books),
    #             'error': str(e)

    #         })
            
    #         return response_json
        
    @app.route('/books/<int:id>', methods=['DELETE'])
    def delete_book(id):
        book = Book.query.get(id)
        if book is None:
            return jsonify({'success': False, 'message': 'Book not found'}), 404

        try:
            book.delete()

            books = Book.query.order_by(Book.id).all()
            current_books = [book.format() for book in books]

            return jsonify({
                'success': True,
                'deleted_id': id,
                'books': current_books,
                'total_books': len(books)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 422



    # @TODO: Write a route that create a new book.
    #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    # TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books.
    #       Your new book should show up immediately after you submit it at the end of the page.
        
    @app.route('/books', methods = ['POST'])
    def add_book():
        data = request.get_json()

        new_title = data.get('title', None)
        new_author = data.get('author', None)
        new_rating = data.get('rating', None)
        search = data.get('search', None)

        try:
            if search:
                selection = Book.query.order_by(Book.id).filter(Book.title.ilike('%{}%'.format(search)))
                current_books = paginate_books(request, selection)

                return jsonify({
                    'success': True,
                    'books': current_books,
                    'total_books': len(selection.all())
                })

            else:
                book = Book(title=new_title, author=new_author, rating=new_rating)
                book.insert()

                selection = Book.query.order_by(Book.id).all()
                current_books = paginate_books(request, selection)


            response_json = json.dumps({
                'books': current_books,
                'success': True,
                'created_id': book.id,
                'total_books': len(Book.query.all())
            }, indent=2)  

            return response_json

        except:
            return jsonify(success=False, error="Book not created"), 422
        

    
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found"
        }), 404
    
    @app.errorhandler(405)
    def wrong_method(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "method not allowed"
        }), 405
    
    @app.errorhandler(422)
    def unprocesable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "unprocessable"
        }), 422

    return app
