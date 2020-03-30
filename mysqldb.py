#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
# Author:linjinting for 02010166
@file: mysqldb.py
@time: 2020/3/28 15:41
'''

import time
from logger.logger import mysql_logger
import MySQLdb
from DBUtils.PooledDB import PooledDB
from MySQLdb.cursors import DictCursor
from MySQLdb import MySQLError
Config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '123456',
    'db': 'gzpw_psm70',
    'charset': 'utf8'
}
start = time.time()
# class mylog:
#     DEBUG = mysql_logger().debug
#     INFO = mysql_logger().info
#     WARNING = mysql_logger().warning
#     ERROR = mysql_logger().error
#     CRITICAL = mysql_logger().critical

RuntimeLevel='DEBUG'
mysql_log = mysql_logger()


def tic():
    return 'at %1.3f seconds' % (time.time() - start)


class PyMySql(object):
    __pool = None

    def __init__(self, **config):
        self.conn = None
        self.cur = None
        self.pool = self.__create_pool(**config)
        print(self.pool)

        self.getConn()
        # print(PyMySql.__pool , self.conn)

        pass

    @staticmethod
    def __create_pool(**config):
        if PyMySql.__pool is None:
            mysql_log.info("create pool")
            PyMySql.__pool = PooledDB(creator=MySQLdb, mincached=1, maxcached=5,
                                      **config, use_unicode=False, cursorclass=DictCursor)

        return PyMySql.__pool

    def getConn(self):
        if self.conn is None:
            self.conn = self.pool.connection()
        if self.cur is None:
            self.cur = self.conn.cursor()

    def select(self, sql):
        rs = 0
        if self.cur is None:
            self.getConn()
        try:
            mysql_log.info('execute --%s'%sql)
            rows = self.cur.execute(sql)
            mysql_log.debug('result rows %s' % rows)
            rs = self.cur.fetchall()

        except MySQLError as e:
            mysql_log.error(e)
            # return 0
        finally:
            print('close')
            self.close()
        return rs

    def close(self):
        try:
            self.cur.close()
        except:
            pass
        try:
            self.conn.close()
        except:
            pass



import threading
import queue


def task_queue(q):
    while True:
        # print("task.get")
        s = q.get()
        if s is None:
            continue
        if s == 'stop':
            break
        threading.Thread(target=select, args=(s['sql'],)).start()
        # print("task.start",s)


def select(sql):
    # pool = PyMySql(**Config)
    print('execute', tic())
    rs = pool.select(sql)
    # for r in rs:
    #     mysql_log.debug('result %s' % r)
    # print(sql, "len:", len(rs))
    pass


def show_th():
    while True:
        print("线程数量是%d" % len(threading.enumerate()))
        time.sleep(1)


if __name__ == '__main__':
    pool = PyMySql(**Config)
    q = queue.Queue()
    threading.Thread(target=task_queue, args=(q,)).start()
    # threading.Thread(target=show_th,).start()
    while True:
        cmd = input("---------\n")
        if cmd == "1":
            print('start', tic())
            sql = 'select * from t_device'
            # select(sql)
            s = {'pool': pool, 'sql': sql}
            for i in range(1):
                q.put(s)

            print("cmd end \n")
        if cmd == "2":
            sql = 'select * from t_user4a'
            s = {'pool': pool, 'sql': sql}
            for i in range(5):
                q.put(s)
        if cmd == 'stop':
            q.put(cmd)
            # time.sleep(0.1)
            break
