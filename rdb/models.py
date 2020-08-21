# Created by Yoo Ju Jin(jujin@100fac.com) 
# Created Date : 2020/08/19
# Copyright (C) 2020, Centum Factorial all rights reserved.
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
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

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return f"<User('{self.name}', '{self.fullname}', '{self.password}')>"


