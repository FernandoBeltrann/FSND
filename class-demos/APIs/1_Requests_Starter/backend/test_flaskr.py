import os
import unittest
import json

from flaskr import create_app
from models import db, setup_db, Book


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        
        self.database_name = "bookshelf_test" # Here the test DB should be put
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "1234", "localhost:5432", self.database_name
        #    usr DB       pw         host:port       DBname 
        )

        self.app = create_app(self.database_path)
        self.client = self.app.test_client
        #setup_db(self.app, self.database_path)

        self.new_book = {
            'title': "Anansi Boys", 
            'author': "Neil Gaiman", 
            'rating': 5
        }

        # binds the app to the current context
        #with self.app.app_context():
            # create all tables
        #    db.create_all()

    def tearDown(self):
        #Excecuted after 
        with self.app.app_context():
            db.session.remove()


# @TODO: Write at least two tests for each endpoint - one each for success and error behavior.
#        You can feel free to write additional tests for nuanced functionality,
#        Such as adding a book without a rating, etc.
#        Since there are four routes currently, you should have at least eight tests.
# Optional: Update the book information in setUp to make the test database your own!
    
    def test_get_paginated_books(self):
        res = self.client().get('/books')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/books?page=1000')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_book_rating(self):
        res = self.client().patch('/books/5', json={'rating':1})
        data = json.loads(res.data)
        with self.app.app_context():
            book = Book.query.filter(Book.id == 5).one_or_none()

        #book = Book.query.filter(Book.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(book.format()['rating'], 1)

    def test_400_for_failed_update(self):
        headers = {
        'Content-Type': 'application/json'
        }
        
        res = self.client().patch('/books/5',headers=headers)  # There seems to be a typo in the URL: '/boks/5' should be '/books/5'
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_delete_book(self):
        with self.app.app_context():
        # Create a new book to be deleted
            book = Book(title="Anansi Boys", author="Neil Gaiman", rating=5)
            book.insert()
            book_id = book.id

        res = self.client().delete(f'/books/{book_id}')
        data = json.loads(res.data)

        with self.app.app_context():
            book = Book.query.filter(Book.id == book_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], book_id)  # Assuming the response contains the 'deleted' key with the ID of the deleted book
        self.assertTrue(data['total_books'])  # This asserts that 'total_books' key exists and is not zero or empty
        self.assertTrue(len(data['books']))  # This asserts that there is a non-zero number of books in the response
        self.assertIsNone(book)  # This asserts that the book with ID 1 is no longer in the database

    def test_422_if_book_does_not_exist(self):
        res = self.client().delete('/books/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Book not found')

    def test_create_new_book(self):
        res = self.client().post('/books', json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('created_id' in data)
        self.assertTrue(len(data['books']) > 0)

    def test_405_if_book_creation_not_allowed(self):
        res = self.client().post('/books/45', json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
