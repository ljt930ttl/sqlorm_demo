#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2020/3/26 15:31
# @Author  : linjinting
# @Site    : 
# @Software: tools-gzpw
# @File    : sessionmaker.py
# @Function:
import asyncio

from table import *
from unit.generate_sql import *

import aiodb
from basemodel import Model

class query(object):
    def __init__(self,tableClass,engine,loop=None):
        self.engine = engine
        self.__loop__ = loop

        self.tableClass = tableClass
        self.__sql_filter__ = None
        self.filter_arg = []
        self.__sql_select__ = tableClass.__select__
        self.__sql__ = self.__sql_select__
    def commit(self):
        if self.__loop__:
            results = self.__loop__.run_until_complete(self.engine.execute(self.__sql__, self.filter_arg))

            return results
    def all(self):
        if self.__loop__:
            results = self.__loop__.run_until_complete(self.engine.select(self.__sql__, self.filter_arg))
            return [self.tableClass(**r) for r in results]

    def filter(self, *args,link=' AND '):
        self.__sql_filter__, self.filter_arg = gen_filter_exp(self.__sql_filter__, self.filter_arg, *args, link=link)

        self.__sql__ = gen_select_sql(self.__sql_select__, self.__sql_filter__)

        return self

    def update(self, args: object, kwargs: object) -> object:
        expr_ = gen_assign_exp( *args, **kwargs)
        self.__sql__ = gen_update(self.tableClass.__update__,expr_, self.__sql_filter__)

        return self

    def __str__(self):
        return "sql:\n%s\nparameters:\n%s"%(self.__sql__, self.filter_arg)

class Sessionmaker(object):
    def __init__(self,bind=None,loop=None):
        self.engine = bind
        self.__loop__ = loop

    def execute(self,sql,*args):
        if self.__loop__:
            results = self.__loop__.run_until_complete(self.engine.execute(sql,*args))
            return results

    def query(self,tableClass):
        # print(tableClass.__tableName__)
        self.tableClass = tableClass
        self.__query = query(tableClass,engine=self.engine,loop=self.__loop__)
        return self.__query



class User(Model):
    __table__= 'user'
    id = Column(IntegerField(),primary_key=True)
    name = Column(StringField())

def test():
    loop = asyncio.get_event_loop()
    engine = loop.run_until_complete(aiodb.create_engine(loop, host='127.0.0.1', port=3306, user='root', password='123456', db='test_1'))
    session = Sessionmaker(bind=engine,loop=loop)
    q = session.query(User).filter(User.id.not_in([123456,2,3]))

    print(q)

if __name__ == '__main__':
    test()