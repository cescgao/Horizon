# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Nov 2017


cookie_expire = 7 * 24 * 3600
env = 'dev'
login_url = '/#login'


class LazySettings(object):
    def __init__(self):
        self.default = {
            'cookie_expire': cookie_expire,
            'env': env,
            'login_url': login_url,
        }
        try:
            self.constants = __import__('constants')
        except ImportError:
            self.constants = None

    def __getattr__(self, item):
        return getattr(self.constants, item, self.default.get(item))


settings = LazySettings()
