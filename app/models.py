## contains your SQLAlchemy models — 
# Python classes that map directly to database tables.

from enum import unique
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String,text
from sqlalchemy.orm import relationship
from .database import Base

# sqlalchemy models are classes that define the structure of a database table
# this is a sqlalchemy model for the user table 
# it defines the structure of the table in the database
# this is a class that inherits from Base, which is a class from the database module
class Post(Base):
    # __tablename__ is a string that defines the name of the table in the database
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content = Column(String,nullable=False)
    published=Column(Boolean,server_default="True",nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default=text('now()'))

    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable = False)
    
    owner = relationship("User")
    # relationship is 

    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable = False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone = True),
                         nullable = False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey(
        "users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey(
        "posts.id",ondelete="CASCADE"),primary_key=True)



''' this models.py file is used to define the structure of the database tables
'''

