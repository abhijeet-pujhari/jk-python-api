# Database models

from sqlalchemy import Column, Integer, String, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    year_published = Column(Integer, nullable=False)
    summary = Column(String)
    reviews = relationship('Review', back_populates='book', cascade='all, delete-orphan')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'))
    user_id = Column(String, nullable=False)
    review_text = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    book = relationship('Book', back_populates='reviews')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    __table_args__ = (UniqueConstraint('username', name='uq_user_username'),)
