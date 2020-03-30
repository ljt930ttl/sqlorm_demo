#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
# Author:linjinting for 02010166
@file: logger.py
@time: 2020/3/29 18:29
'''
import logging
import os
parent = os.path.dirname(os.path.realpath(__file__))
# print(parent)

def mysql_logger():
    # create logger
    # 创建一个日志器logger并设置其日志级别为DEBUG
    logger_mysql = logging.getLogger('mysql')
    logger_mysql.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    # 创建一个流处理器handler并设置其日志级别为DEBUG
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter
    # 创建一个格式器formatter并将其添加到处理器handler
    formatter = logging.Formatter('[%(levelname)s]: %(asctime)s - %(message)s - %(module)s')
    # add formatter to ch
    # 为日志器logger添加上面创建的处理器handler
    ch.setFormatter(formatter)
    # add ch to logger
    logger_mysql.addHandler(ch)
    ##########################################################
    fh = logging.FileHandler(parent + '/mysql_error.log')
    fh.setLevel(logging.ERROR)
    formatter_f = logging.Formatter(
        '[%(levelname)s]: %(asctime)s - %(module)s at %(lineno)d rows\nmsg : %(message)s')
    fh.setFormatter(formatter_f)
    logger_mysql.addHandler(fh)
    ##########################################################
    fh_debug = logging.FileHandler(parent + '/mysql_debug.log')
    fh_debug.setLevel(logging.DEBUG)
    formatter_f = logging.Formatter(
        '[%(levelname)s]: %(asctime)s - %(module)s at %(lineno)d rows\nmsg : %(message)s')
    fh_debug.setFormatter(formatter_f)
    logger_mysql.addHandler(fh_debug)

    return logger_mysql


if __name__ == '__main__':
    logger = mysql_logger()
    # 'application' code
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')


    # import time ,datetime
    # ct = time.time()
    # print(ct)
    # lt = time.localtime(ct)
    # print(lt)
    # # st = time.strftime("%H:%M:%S.%f",lt)
    # print(datetime.datetime.now())