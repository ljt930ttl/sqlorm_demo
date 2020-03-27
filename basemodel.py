#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2020/3/26 13:57
# @Author  : linjinting
# @Site    :
# @Software: tools-gzpw
# @File    : basemodel.py
# @Function:
# from table import Column
from table import *


class BaseModel(type):
    def __new__(cls, name, bases, attrs):

        if 'Model' == name:
            return type.__new__(cls, name, bases, attrs)
        tableName = attrs.get('__table__', None) or name

        primary_key = None
        fields = []
        mappings = dict()
        for key, val in attrs.items():
            if isinstance(val, Column):
                val.name = key
                # mappings[key]=val
                if val.primary_key:
                    if primary_key is not None:
                        raise KeyError('primary_key ')
                    primary_key = key
                else:
                    fields.append(key)
        if primary_key is None:
            raise KeyError('primary_key must be specified')
        # for key in mappings.keys():
        #     attrs.pop(key)
        # primary_keys_str = '`,`'.join(primary_keys)
        fields_str = '`,`'.join(fields)
        # attrs['__mappings__'] = mappings
        attrs['__tableName__'] = tableName
        attrs['primary_key'] = primary_key
        attrs['fields'] = fields

        attrs['__select__'] = 'SELECT `%s`,`%s` FROM `%s`' % (
            primary_key, fields_str, tableName)
        attrs['__update__'] = 'UPDATE `%s`' % (tableName)
        attrs['__delete__'] = 'UPDATE FROM `%s`' % (tableName)
        return type.__new__(cls, name, bases, attrs)


class Model(metaclass=BaseModel):
    def __init__(self, *args, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def __getattr__(self, key):
        # 访问属性不存在则，返回mappings属性
        try:
            return self[key]
        except BaseException:
            raise KeyError('not found ')

    def __setitem__(self, key, value):
        # Let the class subscript access the function self[key]=value
        setattr(self, key, value)

    @classmethod
    def get(cls, pk):
        print(cls.fields)


if __name__ == '__main__':

    class User1(Model):
        __table__ = 'user'
        __slots__ = ()
        id = Column(IntegerField(), primary_key=True)
        name = Column(StringField())
