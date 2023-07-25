from flask import jsonify, json
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..schema import AuthorSchema, AuthorUpdateSchema, BookSchema, BookUpdateSchema
from ..models import Author, Book
from sqlalchemy.exc import IntegrityError

from ..extensions import db, red

author_api = Blueprint('author_api', 'author_api', url_prefix='/api', description='Author Api Routes')



@author_api.route('/author/<int:id>')
class AuthorAPI(MethodView):
    @author_api.response(status_code=200, schema=AuthorSchema)
    def get(self, id):    
        author = Author.query.get_or_404(id)
        return author

    @author_api.arguments(schema=AuthorUpdateSchema)
    @author_api.response(status_code=200, schema=AuthorSchema)
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
        
    
    @author_api.response(status_code=204)
    def delete(self, id):
        author = Author.query.get_or_404(id)
        
        try:
            db.session.delete(author)
            db.session.commit()
            
        except IntegrityError:
            abort(500, message='An error ocurred deleting the author data.')

        else:
            return {'message': 'Author deleted successfully'}
        

@author_api.route('get_all/authors')
class Get_AuthorsAPI(MethodView):
    @author_api.response(status_code=200, schema=AuthorSchema(many=True))
    def get(self):    
        authors = Author.query.all()
        print(authors)
        return authors


@author_api.route('create_author/author')
class Create_AuthorAPI(MethodView):
    @author_api.arguments(schema=AuthorUpdateSchema)
    @author_api.response(status_code=201, schema=AuthorSchema)
    def post(self, author_data):
        author = Author(**author_data)
        
        try:
            db.session.add(author)
            db.session.commit()
        
        except IntegrityError:
            abort(500, message='An error ocurred creating the author data. ')
        
        else:
            return author
