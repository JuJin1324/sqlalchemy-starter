# Created by Yoo Ju Jin(jujin@100fac.com) 
# Created Date : 2020/08/19
# Copyright (C) 2020, Centum Factorial all rights reserved.
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Text, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from rdb.config import engine

Base = declarative_base()


def create_all_tables():
    User.metadata.create_all(engine)


def delete_all_tables():
    User.__table__.drop(engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence(__tablename__ + '_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(50))
    addresses = relationship("Address",
                             backref=backref('user', order_by='Address.id'),
                             cascade="all, delete, delete-orphan")

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return f"<User('{self.name}', '{self.fullname}', '{self.password}')>"


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, email_address):
        self.email_address = email_address

    def __repr__(self):
        return f"<Address({self.email_address})>"


post_keywords = Table('post_keywords', Base.metadata,
                      Column('post_id', Integer, ForeignKey('posts.id')),
                      Column('keyword_id', Integer, ForeignKey('keywords.id'))
                      )


class BlogPost(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)

    keywords = relationship('Keyword', secondary=post_keywords, backref='posts')
    author = relationship('User', backref=backref('posts', lazy='dynamic'))

    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body

    def __repr__(self):
        return f"<BlogPost('{self.headline}', '{self.body}', '{self.author}'>"


class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)

    def __init__(self, keyword):
        self.keyword = keyword
