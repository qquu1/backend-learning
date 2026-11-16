from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    year = Column(Integer, nullable=True)
    author = relationship("Author") #чтобы можно было обращаться


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
