# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Nov 2017


from exceptionhandler import BaseError, LogicError
import datetime


class ModelHandler(object):
    base_model = None
    base_error = BaseError

    def __init__(self, model):
        self.model = model

    def __getattr__(self, item):

        value = None

        def func():
            return value

        if item.startswith('get_'):
            value = getattr(self.model, item[4:], None)
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, datetime.datetime):
                value = self.time_create(value)
            return func
        else:
            return func

    def set(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self.model, k, v)
        self.model.save()

    def get_own(self, *args):
        data = {}
        for a in args:
            data[a] = getattr(self, 'get_' + a)()
        return data

    def flush(self):
        self.model = self.base_model.objects.get(id=self.get_id())

    @classmethod
    def get_by_id(cls, _id):
        return cls.get_by_query(id=_id)

    @classmethod
    def get_by_uid(cls, uid):
        return cls.get_by_query(uid=uid)

    @classmethod
    def get_by_query(cls, **query):
        try:
            return cls(cls.base_model.objects.get(**query))
        except cls.base_model.DoesNotExist:
            raise cls.base_error(cls.__name__ + 'DoesNotExist')
        except cls.base_model.MultipleObjectsReturned:
            raise cls.base_error(cls.__name__ + 'MultipleObjectsReturned')

    @classmethod
    def filter_by_query(cls, *args, **kwargs):
        return cls.base_model.objects.filter(*args, **kwargs)

    @classmethod
    def get_list(cls, *args, **kwargs):
        data = list()
        for s in cls.base_model.objects.filter(**kwargs):
            model = cls(s)
            data.append({a: getattr(model, 'get_' + a)() for a in args})
        return data

    @classmethod
    def create(cls, **kwargs):
        return cls(cls.base_model.objects.create(**kwargs))

    @classmethod
    def create_with_uid(cls, length=10, **kwargs):
        model = cls.base_model(**kwargs)
        retry = 3
        while retry:
            model.uid = cls.generate_hash_uuid(length)
            try:
                model.save()
                break
            except Exception, e:
                print e
                retry -= 1
        if retry:
            return cls(model)
        else:
            raise LogicError('Create error')

    @classmethod
    def get_or_create(cls, **kwargs):
        model, _ = cls.base_model.objects.get_or_create(**kwargs)
        return cls(model)

    @staticmethod
    def execute_raw(raw):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(raw)
        cursor.close()

    @staticmethod
    def query_raw(raw):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(raw)
        data = cursor.fetchall()
        cursor.close()
        return data

    @staticmethod
    def execute_raw_safe(raw, params=()):
        # 通过这种方式做的raw_sql 查询中的参数会被自动转义
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(raw, params)
        cursor.close()

    @staticmethod
    def query_raw_safe(raw, params=()):
        # 通过这种方式做的raw_sql 查询中的参数会被自动转义
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(raw, params)
        data = cursor.fetchall()
        cursor.close()
        return data
