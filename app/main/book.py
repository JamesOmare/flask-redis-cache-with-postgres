from flask import jsonify, json
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..schema import AuthorSchema, AuthorUpdateSchema, BookSchema, BookUpdateSchema
from ..models import Author, Book
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload  # Import joinedload
from ..extensions import db, red
import ast

book_api = Blueprint('book_api', 'book_api', url_prefix='/api', description='Book Api Routes')



@book_api.route('/book/<int:id>')
class BookAPI(MethodView):
    # The response must have the structure of the corresponding Schema
    
    @book_api.response(status_code=200, schema=BookSchema)
    def get(self, id):    
        # try to find if book is in redis cache
        book_key = f"book:{id}"
        cached_book = red.hgetall(book_key)
        
        
        if cached_book:
            
            # If book is found in Redis, return it
            book_data = {
                key.decode(): json.loads(value.decode()) for key, value in cached_book.items()
            }
            
            # Update the 'returned_from' key to 'Redis' since we're getting the data from Redis
            book_data['returned_from'] = 'Redis'
            
            # Save the updated returned_from data back to Redis
            red.hset(book_key, mapping={key: json.dumps(value) for key, value in book_data.items()})
            
            return book_data
            
        else:
            # If book is not in Redis, query it from the database
            book_data = Book.query.get_or_404(id)
            
            
            # Function to convert Author object to dictionary
            def author_to_dict(author):
                if author:
                    return AuthorSchema().dump(author)
                # or
                #     return {
                #         'id': author.id,
                #         'name': author.name,
                #         'book_id': author.book_id,
                #     }
                
                else:
                    return {}
               
                
            if book_data:
                book_data = {
                    'id': book_data.id,
                    'name': book_data.name,
                    'price': book_data.price,
                    # Convert authors to a list of dictionaries
                    'authors':[author_to_dict(author) for author in book_data.authors if author],  
                    # since it did not exist in redis but was found in the database
                    'returned_from': 'Database'
                    }
             
                
                # Convert each value to a JSON string before storing
                book_data_str = {key: json.dumps(value) for key, value in book_data.items()}
                
                
                # Convert book_data values to bytes before storing in Redis
                red.hmset(book_key, book_data_str)
                 
                
                return book_data
        

    @book_api.arguments(schema=BookUpdateSchema)
    @book_api.response(status_code=200, schema=BookSchema)
    def put(self, book_data, id):
        # update the record in the databse
        book = Book.query.get(id)
        
        if book:
            # if the item exist update it
            book.price = book_data['price']
            book.name  = book_data['name'] 
            

        else:
            abort(404, message='A book with that id does not exists. ')

        try:
            # save the changes to the database
            db.session.commit()
        
        except IntegrityError:
            abort(500, message='An error ocurred updating the book data.')

        else:
            
            # try to find if the book is in redis cache
            book_key = f"book:{id}"
            cached_book = red.hgetall(book_key)
            
            if cached_book:
                
                # If book is found in Redis, return it
                book_data = {
                    key.decode(): json.loads(value.decode()) for key, value in cached_book.items()
                }
                
                # Update the 'name' and 'price' key
                book_data['name'] = book.name
                book_data['price'] = book.price
                
                # Save the updated keys data to Redis
                red.hset(book_key, mapping={key: json.dumps(value) for key, value in book_data.items()})
                
                # return the updated book from database
                return book
                
            else:
                # If book is not in Redis, query it from the database, save the record
                # and update the record in the database
                book_data = Book.query.get_or_404(id)

                    
                if book_data:
                    book_data = {
                        'id': book_data.id,
                        'name': book_data.name,
                        'price': book_data.price,
                        'authors':[],
                        # since it did not exist in redis but was found in the database
                        'returned_from': 'Database'
                        }
                
                    
                    # Convert each value to a JSON string before storing
                    book_data_str = {key: json.dumps(value) for key, value in book_data.items()}
                    
                    
                    # Convert book_data values to bytes before storing in Redis
                    red.hmset(book_key, book_data_str)
                    
                    # return the updated book from database
                    return book
        
        
        
        
    
    @book_api.response(status_code=204)
    def delete(self, id):
        book = Book.query.get_or_404(id)
        
        try:
            db.session.delete(book)
            db.session.commit()
            
        except IntegrityError:
            abort(500, message='An error ocurred deleting the book data.')

        else:
            return {'message': 'Book deleted successfully'}
        

@book_api.route('get_all/books')
class Get_BooksAPI(MethodView):
     @book_api.response(status_code=200, schema=BookSchema(many=True))
     def get(self):
        return Book.query.all()


@book_api.route('create_book/book')
class Create_BookAPI(MethodView):
    @book_api.arguments(schema=BookUpdateSchema)
    @book_api.response(status_code=201, schema=BookSchema)
    def post(self, book_data):
        book = Book(**book_data)
        
        try:
            db.session.add(book)
            db.session.commit()
        
        except IntegrityError:
            abort(500, message='An error ocurred creating the book data. ')
        
        else:

            # set the book key as the created book id
            book_key = f"book:{book.id}"
            
        
            # Since a new book has been created in the db, store it in redis as well as a hash
            if book:
                book_data = {
                'id': book.id,
                'name': book.name,
                'price': book.price,
                'authors':[],
                'returned_from': 'Database'
                }
                
                # Convert each value to a JSON string before storing
                book_data_str = {key: json.dumps(value) for key, value in book_data.items()}

                # Convert book_data values to bytes before storing in Redis
                red.hmset(book_key, book_data_str)
                
                # return the created book from database
                return book
            
            abort(404, message='The book does not exist. ')
            
            
       

