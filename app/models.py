from datetime import datetime
from .extensions import db

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    book_id = db.Column(db.ForeignKey("book.id", ondelete = 'CASCADE'))

    book = db.relationship("Book", back_populates="authors", passive_deletes = True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return 'Author %r' % self.name


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Float, nullable=False)

    authors = db.relationship("Author", back_populates="book", passive_deletes = True)  

    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow) 

    def __repr__(self):
        return 'Book %r' % self.name
