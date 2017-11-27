# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Nov 2017


from codex import ModelHandler, utils
from codex.exceptionhandler import AuthError
from constants import cookie_expire
from .models import *


class Passport(ModelHandler):
    base_error = AuthError
    base_model = ObjAccessToken

    @classmethod
    def login(cls, handler, user):
        access_token = utils.sha1(user['username'] + utils.generate_hash_limit())
        m = ObjAccessToken.objects.create(
            uid=user['uid'], access_token=access_token,
            expire=utils.get_datetime_now() + utils.timedelta(seconds=cookie_expire)
        )
        signature = utils.sha1(handler.ip + str(utils.to_timestamp(m.expire)))
        handler.set_cookie.update({'passport': access_token, 'signature': signature})
        model = cls(m)
        data = {'ip': handler.ip, 'host': handler.host}
        data.update(user)
        model.set(data=data)
        return model

    @classmethod
    def logout(cls, handler):
        handler.delete_cookie += ['passport', 'signature']

    def verify(self):
        if self.model.user_id and self.model.expire < utils.get_datetime_now():
            raise AuthError('Expired')
        return self.model.data


def login_required(func):

    def func_wrapper(cls, *_args, **_kwargs):
        access_token = cls.request.COOKIES.get('passport')
        if not access_token:
            raise AuthError('Invalid Identity')
        token = Passport.get_by_query(access_token=access_token)
        cls.request.user = token.verify()
        cls.request.token = token
        return func(cls, *_args, **_kwargs)

    return func_wrapper
