# import datetime as dt
# from dataclasses import dataclass

# from marshmallow import Schema, fields


# # author
# class AuthorSchema(Schema):
#     id  = fields.Int(dump_only=True)
#     name = fields.Str(required=True)

# class AuthorUpdateSchema(Schema):
#     name = fields.Str(required=True)
#     book_id = fields.Int()
    
# # book
# class BookSchema(Schema):
#     id  = fields.Int(dump_only=True)
#     name = fields.Str(required=True)
#     price = fields.Float(required=True)
#     authors = fields.Nested(AuthorSchema, many=True)
    
# class BookUpdateSchema(Schema):
#     name = fields.Str(required=True)
#     price = fields.Float(required=True)
    

from marshmallow import Schema, fields, validate

class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))
    book_id = fields.Int()

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=50))
    price = fields.Float(required=True)
    authors = fields.Nested(AuthorSchema, many=True)
    returned_from = fields.Str(required=True, default='Database')

class BookUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(max=50))
    price = fields.Float(required=True)

class AuthorUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(max=100))
    # Make the 'book_id' field optional
    book_id = fields.Int(missing=None, allow_none=True)  

    
