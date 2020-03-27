#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2020/3/25 18:35
# @Author  : linjinting
# @Site    : 
# @Software: tools-gzpw
# @File    : table.py
# @Function:


class Column(object):

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop("name", None)
        self.type_ = kwargs.pop("type_", None)
        self.value = None
        args = list(args)
        if args:
            if isinstance(args[0], str):
                if self.name is not None:
                        raise KeyError(
                        "May not pass name positionally and as a keyword."
                    )
                self.name = args.pop(0)
        if args:
            coltype = args[0]

            if hasattr(coltype, "_sqla_type"):
                if self.type_ is not None:
                    raise KeyError(
                        "May not pass type_ positionally and as a keyword."
                    )
                self.type_ = args.pop(0)

        self.key = kwargs.pop("key", self.name)
        self.primary_key = kwargs.pop("primary_key", False)
        self.default = kwargs.pop("default", None)
        self.server_default = kwargs.pop("server_default", None)

    def not_in(self,arg):
        return (self.name, tuple(arg), ' NOT IN ')

    def in_(self,arg):
        return (self.name, arg, ' IN ')

    def between(self,*arg):
        ## key, val,symbol
        symble =  'BETWEEN %s AND'
        return (self.name, arg, symble)

    def like(self,arg):
        return (self.name, arg," LIKE ")
        pass

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.type_, self.name)

    def __eq__(self, other):
        # print(self.name)
        # expression = "`%s` = %%s"%(self.name)
        return (self.name, str(other),"=")

    def __ne__(self, other):
        return (self.name, str(other),"<>")

    def __ge__(self,other):
        if not isinstance(other, int):
            raise TypeError("right value(%s) type must be 'int'"%other)
        return (self.name, str(other), ">=")

    def __le__(self, other):
        if not isinstance(other, int):
            raise TypeError("right value(%s) type must be 'int'"%other)
        return (self.name, str(other), "<=")

    def __gt__(self, other):
        if not isinstance(other, int):
            raise TypeError("right value(%s) type must be 'int'"%other)
        return (self.name, str(other), ">")

    def __lt__(self, other):
        if not isinstance(other, int):
            raise TypeError("right value(%s) type must be 'int'"%other)
        return (self.name, str(other), "<")

    def __invert__(self):
        return self

class Field(object):
    _sqla_type = True
    def __init__(self,type=None,length=None):
        self.length = length
        self.type = type

    def __str__(self):
        if self.length is None:
            return '%s' % (self.type)
        return '%s(%s)' % (self.type, self.length)

class StringField(Field):
    __visit_name__ = "string"
    def __init__(self, length=None,collation=None, convert_unicode=False,):
        # super().__init__(name, ddl, primary_key, default)
        self.length = length
        self.collation = collation
        self.type='VARCHAR'
        super().__init__(self.type, self.length)


class BooleanField(Field):
    __visit_name__ = "boolean"
    def __init__(self, length=None,collation=None, convert_unicode=False,):
        # super().__init__(name, ddl, primary_key, default)
        self.length = length
        self.collation = collation
        self.type='VARCHAR'
        super().__init__(self.type, self.length)

class IntegerField(Field):
    __visit_name__ = "integer"
    def __init__(self):
        self.type='INTEGER'
        super().__init__(self.type)

class FloatField(Field):
    __visit_name__ = "float"
    def __init__(self, precision):
        # super().__init__(name, ddl, primary_key, default)
        self.precision = precision
        self.type='VARCHAR'
        super().__init__(self.type)

class TextField(StringField):
    __visit_name__ = "text"
