#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2020/3/26 19:28
# @Author  : linjinting
# @Site    : 
# @Software: tools-gzpw
# @File    : generate_sql.py
# @Function:

def gen_filter_exp(sql_filter_, arg_, *filter, link=' AND '):
    filters_ = []
    for key, val,symbol in filter:
        filter_ = "`%s` %s %%s"%(key, symbol)
        if isinstance(val,tuple):
         arg_.extend(val)
        else:
            arg_.append(val)
        filters_.append(filter_)
    expression_ = link.join(filters_)

    if sql_filter_ is None:
        return expression_,arg_
    else:
        return sql_filter_ + link + expression_, arg_

def gen_assign_exp(*args, **kwargs):
    expressions = []
    for arg in args:
        for key, val in arg.items():
            # set key = val
            expression_ = "`%s` = '%s'" % (key, val)
            expressions.append(expression_)
    for key, val in kwargs.items():
        # set key = val
        expression_ = "`%s` = '%s'" % (key, val)
        expressions.append(expression_)
    assign_exp = ', '.join(expressions)

    return assign_exp

def gen_select_sql(sql_, filter_):
    return sql_+' WHERE ' + filter_

def gen_update(sql_, assign_, filter_):
    return sql_ +' SET '+ assign_ + ' WHERE ' + filter_

def gen_delete_sql(sql_, filter_):
    return sql_+' WHERE ' + filter_

def gen_insert_sql(sql_,column_):
    return sql_+ column_
