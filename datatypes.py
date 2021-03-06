#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'pandazxx'

import collections


class ArrayObject(object):
    def __init__(self, element_type=object):
        assert callable(element_type)
        self.__element_type = element_type

    @property
    def element_type(self):
        return self.__element_type


class DictData(object):
    def __init__(self, **kwargs):
        if not kwargs or len(kwargs) == 0:
            return
        required_attr_names = [x for x in dir(self) if not x.startswith('_')]
        for attr_name in required_attr_names:
            attr = getattr(self.__class__, attr_name)
            if callable(attr) \
                    or isinstance(attr, type)\
                    or type(attr) is property:
                continue
            if not attr_name in kwargs:
                raise AttributeError('Required attribute "{0}" not found'.format(attr_name))
            value = kwargs[attr_name]
            if isinstance(attr, DictData):
                if not isinstance(value, type(kwargs)):
                    raise TypeError('Wrong type of value found when building <{class_name}> attribute "{attr_name}", '
                                    'required <{required_type}>, '
                                    'found <{real_type}>'.format(class_name=type(attr).__name__,
                                                                 attr_name=attr_name,
                                                                 required_type=type(kwargs).__name__,
                                                                 real_type=type(value).__name__))
                self.__dict__[attr_name] = type(attr)(**value)
            elif isinstance(attr, ArrayObject):
                if not isinstance(value, collections.Iterable):
                    raise TypeError('Wrong type of value found when building <{class_name}> attribute "{attr_name}", '
                                    'required <{required_type}>, '
                                    'found <{real_type}>'.format(class_name=type(attr).__name__,
                                                                 attr_name=attr_name,
                                                                 required_type=collections.Iterable.__name__,
                                                                 real_type=type(value).__name__))
                values = []
                for item in value:
                    if not isinstance(item, type(kwargs)):
                        raise TypeError(
                            'Wrong type of value found when building <{class_name}> attribute "{attr_name}", '
                            'required <{required_type}>, '
                            'found <{real_type}>'.format(class_name=type(attr).__name__,
                                                         attr_name=attr_name,
                                                         required_type=type(kwargs).__name__,
                                                         real_type=type(item).__name__))
                    i = attr.element_type(**item)
                    values.append(i)
                self.__dict__[attr_name] = values
            else:
                self.__dict__[attr_name] = value
        for remaining_attr_name in kwargs.keys() - required_attr_names:
            if remaining_attr_name.startswith('_'):
                continue
            self.__dict__[remaining_attr_name] = kwargs.get(remaining_attr_name, None)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        props = self.__dict__.copy()
        for key, value in props.items():
            if isinstance(value, DictData):
                props[key] = value.to_dict()
        return props


def main():
    class TestCls1(DictData):
        required1 = None
        required2 = DictData()
        required3 = {}

        def not_required1(self): print("not_required1")

        def _not_required2(self): print("_not_required2")

        __not_required3 = '__not_required3'

        def test_desc(self):
            print('required1: {0}'.format(str(self.required1)))
            print('required2: {0}'.format(str(self.required2)))
            print('required3: {0}'.format(str(self.required3)))
            print('not_required1: {0}'.format(str(self.not_required1)))
            print('_not_required2: {0}'.format(str(self._not_required2)))
            print('__not_required3: {0}'.format(str(self.__not_required3)))
            print('dict: {0}'.format(str(self.to_dict())))

    class TestCls2(DictData):
        list1 = ArrayObject(TestCls1)

        def test_desc(self):
            print("List items:")
            for l in self.list1:
                print('\t# {0}'.format(l))

    dict1 = {
        'required1': 'required1_val',
        'required2': {'extra1': 'extra1_val'},
        'required3': {'required3': 'required3_val'},
        'not_required1': "not_required1_val",
        '_not_required2': "_not_required2_val",
        '__not_required3': '__not_required3_val',
        'extra2': 'extra2_val',
        '_extra3': 'extra3_val',
    }

    dict2 = {
        'required1': 'required1_val',
        'required2': 'required2_val',
        'required3': {'required3': 'required3_val'},
        'not_required1': "not_required1_val",
        '_not_required2': "_not_required2_val",
        '__not_required3': '__not_required3_val',
        'extra2': 'extra2_val',
    }

    dict3 = {
        'required2': {'extra1': 'extra1_val'},
        'required3': {'required3': 'required3_val'},
        'not_required1': "not_required1_val",
        '_not_required2': "_not_required2_val",
        '__not_required3': '__not_required3_val',
        'extra2': 'extra2_val',
    }

    dict4 = {
        'list1': [
            dict1.copy(),
            dict1.copy(),
            dict1.copy(),
        ]
    }

    dict5 = {
        'list1': [
            dict1.copy(),
            dict1.copy(),
            "",
        ]
    }
    try:
        print("*"*10 + " Test1")
        t1 = TestCls1(**dict1)
        t1.test_desc()
        print('t1.required2.extra1: {0}'.format(t1.required2.extra1))
    except Exception as e:
        import traceback
        print(e)
        traceback.print_exc()
    try:
        print("*"*10 + " Test2")
        t1 = TestCls1(**dict2)
        t1.test_desc()
        print('t1.required2.extra1: {0}'.format(t1.required2.extra1))
    except Exception as e:
        import traceback
        print(e)
        traceback.print_exc()
    try:
        print("*"*10 + " Test3")
        t1 = TestCls1(**dict3)
        t1.test_desc()
        print('t1.required2.extra1: {0}'.format(t1.required2.extra1))
    except Exception as e:
        import traceback
        print(e)
        traceback.print_exc()

    try:
        print("*"*10 + " Test4")
        t1 = TestCls2(**dict4)
        t1.test_desc()
    except Exception as e:
        import traceback
        print(e)
        traceback.print_exc()

    try:
        print("*"*10 + " Test5")
        t1 = TestCls2(**dict5)
        t1.test_desc()
    except Exception as e:
        import traceback
        print(e)
        traceback.print_exc()

if __name__ == '__main__':
    main()
