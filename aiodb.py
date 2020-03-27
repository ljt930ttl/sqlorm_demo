#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2020/3/23 10:56
# @Author  : linjinting
# @Site    : 
# @Software: tools-gzpw
# @File    : aiodb.py
# @Function:

import aiomysql
from pymysql.err import MySQLError
import asyncio
import logging
import sys

'''
mysql 异步版本
'''

logobj = logging.getLogger('mysql')
logobj.setLevel(logging.INFO) #日志等级为ERROR

loghead = logging.StreamHandler(sys.stderr)
logobj.addHandler(loghead)

class Pmysql:
    def __init__(self):
        self.coon = None
        self.pool = None

        self.autocommit = None

    async def initpool(self, loop, **kwargs):

        host = kwargs.get('host', 'localhost')
        port = kwargs.get('port', 3306)
        user = kwargs['user']
        password = kwargs['password']
        db = kwargs.get('db')
        charset = kwargs.get('charset', 'utf8')
        self.autocommit = autocommit = kwargs.get('autocommit', True)
        maxsize = kwargs.get('maxsize', 10)
        minsize = kwargs.get('minsize', 1)

        try:
            logobj.debug("will connect mysql~")
            __pool = await aiomysql.create_pool(
                host=host,
                port=port,
                user=user,
                password=password,
                db=db,
                charset=charset,
                autocommit=autocommit,
                maxsize=maxsize,
                minsize=minsize,
                loop=loop)

            return __pool
        except:
            logobj.error('connect error.', exc_info=True)
            return

    async def select(self, sql, args=None, size=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql, args)
                if size:
                    rs = await cur.fetchmany(size)
                else:
                    rs = await cur.fetchall()
            logobj.info('rows returned: %s' % len(rs))
            return rs

    async def execute(self, sql, args):
        async with self.pool.acquire() as conn:
            if not self.autocommit:
                await conn.begin()
            try:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(sql, args)
                    affected = cur.rowcount
                if not self.autocommit:
                    await conn.commit()
            except MySQLError as e:
                if not self.autocommit:
                    await conn.rollback()
                # raise
                affected = e.args[0]
                # print(e)
            return affected


async def create_engine(loop,**kwargs):
    _engine = Pmysql()
    _engine.pool = await _engine.initpool(loop, **kwargs)
    return _engine





if __name__ == '__main__':
    pass

