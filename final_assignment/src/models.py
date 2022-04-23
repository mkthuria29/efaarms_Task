import sqlalchemy as db
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    full_name = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean(), default=True)


class Book(Base):
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    published = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean(), default=True)


class FavouriteBook(Base):
    user_id = db.Column(db.String(36), nullable=False)
    book_id = db.Column(db.String(36), nullable=False)
    like = db.Column(db.Boolean)

    book = relationship("Book", primaryjoin="FavouriteBook.book_id==Book.id", foreign_keys=book_id)
