# from flask import jsonify, json
# from flask.views import MethodView
# from flask_smorest import Blueprint, abort
# from ..schema import AuthorSchema, AuthorUpdateSchema, BookSchema, BookUpdateSchema
# from ..models import Author, Book
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import joinedload  # Import joinedload
# from ..extensions import db, red
# import ast

# book_api = Blueprint('book_api', 'book_api', url_prefix='/api', description='Book Api Routes')



# @book_api.route('/book/<int:id>')
# class BookAPI(MethodView):
#     # The response must have the structure of the corresponding Schema
    
#     @book_api.response(status_code=200, schema=BookSchema)
#     def get(self, id):    
#         # try to find if book is in redis cache
#         book_key = f"book:{id}"
#         cached_book = red.hgetall(book_key)
        
        
#         if cached_book:
#             # If book is found in Redis, return it
#             book_data = {
#                 key.decode(): json.loads(value.decode()) for key, value in cached_book.items()
#             }
#             return book_data
#             # If book is found in Redis, return it
#             decoded_cached_book = {field.decode(): value.decode() for field, value in cached_book.items()}
            
#             # Convert authors back to list
#             decoded_cached_book['authors'] = json.loads(decoded_cached_book['authors'])  
            
#             return decoded_cached_book
            
#         else:
#             # If book is not in Redis, query it from the database
#             book_data = Book.query.get_or_404(id)
            
            
#             # Function to convert Author object to dictionary
#             def author_to_dict(author):
#                 if author:
#                     # return AuthorSchema().dump(author)
#                     return {
#                         'id': author.id,
#                         'name': author.name,
#                         'book_id': author.book_id,
#                     }
#                 else:
#                     return {}
                
#             if book_data:
#                 book_data = {
#                     'id': book_data.id,
#                     'name': book_data.name,
#                     'price': book_data.price,
#                     # Convert authors to a list of dictionaries
#                     'authors':[author_to_dict(author) for author in book_data.authors if author],  
#                     # 'authors': json.dumps([author_to_dict(author) for author in book_data.authors if author]),  
#                     # since it did not exist in redis but was found in the database
#                     'returned_from': 'Database'
#                     }
#                 # Convert book_data to a JSON string with ensure_ascii=False
#                 # book_data_json = json.dumps(book_data, ensure_ascii=False)
                
#                 # Store book_data in Redis using hset
#                 # red.hset(book_key, "book_data", book_data_json)
                
                
#                 for key, value in book_data.items():
#                     # Convert value to a JSON string before storing
#                     value_str = json.dumps(value)
#                     red.hset(book_key, key, value_str)
                
#                 # Convert each value in book_data to a string representation
#                 # book_data_str = {key: json.dumps(value) for key, value in book_data.items()}
                
#                 # Convert authors to JSON string
#                 # book_data_str['authors'] = json.dumps(book_data_str['authors'])
                
#                 # Convert book_data values to bytes before storing in Redis
#                 # red.hmset(book_key, book_data_str)
                 
                
#                 return book_data
               
                
               
                 
                
#                 return book_data
#             else:
#                 return None
        

#     @book_api.arguments(schema=BookUpdateSchema)
#     @book_api.response(status_code=200, schema=BookSchema)
#     def put(self, book_data, id):
#         book = Book.query.get(id)
#         if book:
#             # if the item exist update it
#             book.price = book_data['price']
#             book.name  = book_data['name'] 

#         else:
#              abort(404, message='A book with that id does not exists. ')

#         try:
#             db.session.commit()
        
#         except IntegrityError:
#             abort(500, message='An error ocurred updating the book data.')

#         else:
#             return book
    
#     @book_api.response(status_code=204)
#     def delete(self, id):
#         book = Book.query.get_or_404(id)
        
#         try:
#             db.session.delete(book)
#             db.session.commit()
            
#         except IntegrityError:
#             abort(500, message='An error ocurred deleting the book data.')

#         else:
#             return {'message': 'Book deleted successfully'}
        

# @book_api.route('get_all/books')
# class Get_BooksAPI(MethodView):
#      @book_api.response(status_code=200, schema=BookSchema(many=True))
#      def get(self):
#         return Book.query.all()