# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# 2017


from .settings import settings
import redis
import utils


class CacheHandler(object):
    def __init__(self, host, port, db, password):
        self.client = redis.Redis(host, port=port, db=db, password=password)

    def get(self, key):
        value = self.client.get(key)
        if value:
            return utils.json_loads(value)

    def set(self, key, value, expire):
        self.client.setex(key, utils.json_dumps(value), expire)

    def api(self, expire):

        def func_wrapper(func):

            def _func_wrapper(cls, *args, **kwargs):

                if cls.request.method.lower() != 'get':
                    return func(cls, *args, **kwargs)
                key = cls.request.path_info + '?' + utils.url_encoder(
                    {k: v.encode('utf-8') for k, v in cls.request.GET.items()})
                if getattr(cls.request, 'user', None):
                    key += utils.url_encoder(cls.request.COOKIES)
                hash_key = key
                if settings.cache:
                    resp = self.get(hash_key)
                    if resp is None:
                        resp = func(cls, *args, **kwargs)
                        self.set(hash_key, resp, expire)
                    else:
                        print 'hit cache: %s' % key
                else:
                    resp = func(cls, *args, **kwargs)
                return resp

            return _func_wrapper

        return func_wrapper

    def clean_api(self, key):
        if settings.cache:
            for k in self.client.keys(key):
                self.client.delete(k)


if settings.cache:
    cache = CacheHandler(
        settings.cache_host, settings.cache_port or 6379, settings.cache_db or 0, settings.cache_password)
else:
    cache = None
