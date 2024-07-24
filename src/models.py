import os
import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base, backref
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

followers = Table('follower',
    Base.metadata,
    Column('user_from_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('user_to_id', Integer, ForeignKey('user.id'), nullable=False),
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    username = Column(String(250), nullable = False)
    firstname = Column(String(250))
    lastname = Column(String(250))
    email = Column(String(250), unique = True)
    followers = relationship('User', secondary=followers, lazy='subquery',
        backref=backref('users', lazy=True))
    
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)

    user = relationship("User")
    
class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key = True)
    type = Column(String(250))
    url = Column(String(250))
    post_id = Column(Integer, ForeignKey('post.id'), nullable = False)
    
    post = relationship("Post")
    
class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key = True)
    comment_text = Column(String(250))
    author_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable = False)
    
    author = relationship("User")
    post = relationship("Post")

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
