# from flask import Flask
# from flask.views import MethodView
# import marshmallow as ma
# from flask_smorest import Api, Blueprint, abort

# from .model import Pet

# app = Flask(__name__)
# app.config["API_TITLE"] = "My API"
# app.config["API_VERSION"] = "v1"
# app.config["OPENAPI_VERSION"] = "3.0.2"
# api = Api(app)


# class PetSchema(ma.Schema):
#     id = ma.fields.Int(dump_only=True)
#     name = ma.fields.String()
    
# class PetQueryArgsSchema(ma.Schema):
#     name = ma.fields.String()
    
# blp = Blueprint("pets", "pets", url_prefix="/pets", description="Operations on pets")


# @blp.route("/")
# class Pets(MethodView):
#     @blp.arguments(PetQueryArgsSchema, location="query")
#     @blp.response(200, PetSchema(many=True))
#     def get(self, args):
#         """List pets"""
#         return Pet.get(filters=args)

#     @blp.arguments(PetSchema)
#     @blp.response(201, PetSchema)
#     def post(self, new_data):
#         """Add a new pet"""
#         item = Pet.create(**new_data)
#         return item


# @blp.route("/<pet_id>")
# class PetsById(MethodView):
#     @blp.response(200, PetSchema)
#     def get(self, pet_id):
#         """Get pet by ID"""
#         try:
#             item = Pet.get_by_id(pet_id)
#         except ItemNotFoundError:
#             abort(404, message="Item not found.")
#         return item

#     @blp.arguments(PetSchema)
#     @blp.response(200, PetSchema)
#     def put(self, update_data, pet_id):
#         """Update existing pet"""
#         try:
#             item = Pet.get_by_id(pet_id)
#         except ItemNotFoundError:
#             abort(404, message="Item not found.")
#         item.update(update_data)
#         item.commit()
#         return item

#     @blp.response(204)
#     def delete(self, pet_id):
#         """Delete pet"""
#         try:
#             Pet.delete(pet_id)
#         except ItemNotFoundError:
#             abort(404, message="Item not found.")


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
# from marshmallow import Marshmallow
import marshmallow as ma
from flask_smorest import Api, Blueprint

# Create the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy database object
db = SQLAlchemy(app)

# Initialize Marshmallow
# ma = Marshmallow(app)

# Create the API Blueprint
api_bp = Blueprint('api', 'api', url_prefix='/api', description='API')

# Initialize the API
api = Api(app)
api.register_blueprint(api_bp)

# Define a simple SQLAlchemy model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

# Create a schema for the Item model
class ItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Item
    
    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()

# Create the marshmallow schema instances
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

# Routes
@api_bp.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify(items_schema.dump(items))

if __name__ == '__main__':
    # Create the database tables (if they don't exist)
    db.create_all()
    app.run(debug=True)
