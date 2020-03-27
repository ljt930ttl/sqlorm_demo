#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2020/3/25 10:22
# @Author  : linjinting
# @Site    : 
# @Software: tools-gzpw
# @File    : test_sqlsm.py
# @Function:

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    ID = Column(Integer, primary_key=True)
    name = Column(String(20))

engine = create_engine('mysql://root:123456@10.7.3.188/test_1')
DBSession = sessionmaker(bind=engine)
session = DBSession()
s = User
user_que= session.query(User).filter(~User.name.like("123%")).update()
print(user_que)