from datetime import datetime
from .extensions import db

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # Add nullable=False
    book_id = db.Column(db.ForeignKey("book.id"), nullable=True)  # Add nullable=False

    book = db.relationship("Book", back_populates="authors")

    def __repr__(self):
        return 'Author %r' % self.name


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    authors = db.relationship("Author", back_populates="authors")  # Use "authors" instead of "author" for consistency

    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Add timestamp field 'created_at'
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Add timestamp field 'updated_at'

    def __repr__(self):
        return 'Book %r' % self.name