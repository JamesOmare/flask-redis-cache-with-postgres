from flask import jsonify, json
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..schema import AuthorSchema, AuthorUpdateSchema, BookSchema, BookUpdateSchema
from ..models import Author, Book
from sqlalchemy.exc import IntegrityError

from ..extensions import db, red

api = Blueprint('api', 'api', url_prefix='/api', description='Api Blueprint')



@api.route('/book/<int:id>')
class BookAPI(MethodView):
    # The response must have the structure of the corresponding Schema
    
    @api.response(status_code=200, schema=BookSchema)
    def get(self, id):    
        book = Book.query.get_or_404(id) # if founded returns item, or raise an abort 404
        return book

    @api.arguments(schema=BookUpdateSchema)
    @api.response(status_code=200, schema=BookSchema)
    def put(self, book_data, id):
        book = Book.query.get(id)
        if book:
            # if the item exist update it
            book.price = book_data['price']
            book.name  = book_data['name'] 

        else:
             abort(404, message='A book with that id does not exists. ')

        try:
            db.session.commit()
        
        except IntegrityError:
            abort(500, message='An error ocurred updating the book data.')

        else:
            return book
    
    @api.response(status_code=204)
    def delete(self, id):
        book = Book.query.get_or_404(id)
        
        try:
            db.session.delete(book)
            db.session.commit()
            
        except IntegrityError:
            abort(500, message='An error ocurred deleting the book data.')

        else:
            return {'message': 'Book deleted successfully'}
        
    
@api.route('/books')
class BooksAPI(MethodView):
    @api.response(status_code=200, schema=BookSchema(many=True))
    def get(self):
        return Book.query.all()

    @api.arguments(schema=BookUpdateSchema)
    @api.response(status_code=201, schema=BookSchema)
    def post(self, book_data):
        print(book_data['name'])
        book = Book(**book_data)
        
        try:
            db.session.add(book)
            db.session.commit()
        
        except IntegrityError:
            abort(500, message='An error ocurred creating the book data. ')
        
        else:
            # book_key = 'book:{id}'.format(id=book.id)
            book_key = f"book:{book.id}"
            # book_data = red.hmset(book.id, {'name': book.name, 'price': book.price})

            cached_book = red.hgetall(book_key)
            
            # if it exists in redis, return the data
            if cached_book:
                return {field.decode('utf-8'): value.decode('utf-8') for field, value in cached_book.items()}

            # if book is not in redis, store it in redis as a hash
            else:
                if book:
                    book_data = {
                    'id': book.id,
                    'name': book.name,
                    'price': book.price,
                    }
                    red.hmset(book_key, book_data)
                    return book
                
                abort(404, message='The book does not exist. ')
            
            
       
    
@api.route('/author/<int:id>')
class AuthorAPI(MethodView):
    @api.response(status_code=200, schema=AuthorSchema)
    def get(self, id):    
        author = Author.query.get_or_404(id)
        return author

    @api.arguments(schema=AuthorUpdateSchema)
    @api.response(status_code=200, schema=AuthorSchema)
    def put(self, author_data, id):
        author = Author.query.get(id)
        if author:
            author.name  = author_data['name']
            author.book_id = author_data['book_id']
        
        else:
            abort(404, message='A book with that id does not exists. ')

        try:
            db.session.commit()
            
        except IntegrityError:
            abort(500, message='An error ocurred updating the author data.')
        
        else:
            return author
        
    
    @api.response(status_code=204)
    def delete(self, id):
        author = Author.query.get_or_404(id)
        
        try:
            db.session.delete(author)
            db.session.commit()
            
        except IntegrityError:
            abort(500, message='An error ocurred deleting the author data.')

        else:
            return {'message': 'Author deleted successfully'}
        
        
@api.route('/authors')
class AuthorsAPI(MethodView):
    @api.response(status_code=200, schema=AuthorSchema(many=True))
    def get(self):    
        authors = Author.query.all()
        print(authors)
        return authors

    @api.arguments(schema=AuthorUpdateSchema)
    @api.response(status_code=201, schema=AuthorSchema)
    def post(self, author_data):
        author = Author(**author_data)
        
        try:
            db.session.add(author)
            db.session.commit()
        
        except IntegrityError:
            abort(500, message='An error ocurred creating the author data. ')
        
        else:
            return author
