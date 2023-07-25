from flask import Flask, jsonify
from .config import Config
from .extensions import db, _api
from .main.views import api
from .main.book import book_api
from .main.author import author_api
from flask.views import MethodView


def create_app(config = Config):
    
    #instance relative config tells our flask application that
    #there will be some configurations set up outside the directory
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    # Connect flask app to flask smorest
    _api.init_app(app)
    
    # initialize DB
    db.init_app(app)
    
    # Create tables defined by models if not exists.
    with app.app_context():
        db.create_all()
        
   
    class Hello(MethodView):
        def get(self):
            return jsonify({"Hello": "go to /docs to access the API documentation"})

    # Bind the class-based view to the URL '/'
    app.add_url_rule('/', view_func=Hello.as_view('hello'))
    
    
    #this registers the given blueprint
    # _api.register_blueprint(api)
    _api.register_blueprint(book_api)
    _api.register_blueprint(author_api)

    return app