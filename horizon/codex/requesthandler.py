# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Nov 2017


from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from .exceptionhandler import BaseError, AuthError
from .loghandler import logger
from .settings import settings
from .utils import json_dumps, json_loads, Dict, url_quote
import traceback


class BaseHandler(View):
    def __init__(self, **kwargs):
        super(BaseHandler, self).__init__(**kwargs)
        self.set_cookie = {}
        self.delete_cookie = []
        self.query_or_body = None
        self.ip = ''
        self.host = ''

    def http_method_not_allowed(self, *args, **kwargs):
        return HttpResponseNotAllowed(self._allowed_methods())

    def dispatch(self, request, *args, **kwargs):
        handler = getattr(self, self.request.method.lower(), None)
        if not callable(handler):
            return self.http_method_not_allowed()
        return self.request_wrapper(handler, *args, **kwargs)

    def request_wrapper(self, func, *args, **kwargs):
        self.ip = self.request.META.get('HTTP_X_REAL_IP') or self.request.META.get('HTTP_X_FORWARDED_FOR') \
                  or self.request.META.get('REMOTE_ADDR', '')
        self.host = self.request.META.get('HTTP_HOST', '')
        response = self._request_wrapper(func, *args, **kwargs)
        if self.set_cookie:
            for k, v in self.set_cookie.iteritems():
                response.set_cookie(k, v, expires=settings.cookie_expire, httponly=True)
        if self.delete_cookie:
            for k in self.delete_cookie:
                response.delete_cookie(k)
        return response

    def _request_wrapper(self, func, *args, **kwargs):
        response = HttpResponse(func(*args, **kwargs))
        self.delete_cookie.append('passport')
        return response

    @property
    def body(self):
        return Dict(json_loads(self.request.body)) if self.request.body else Dict({})

    @property
    def query(self):
        d = Dict(getattr(self.request, 'GET').iteritems())
        d.update(getattr(self.request, 'POST').iteritems())
        d.update(getattr(self.request, 'FILES').iteritems())
        return d

    @property
    def input(self):
        if self.query_or_body is None:
            self.query_or_body = self.query or self.body
        return self.query_or_body


class ApiHandler(BaseHandler):
    def _request_wrapper(self, func, *args, **kwargs):
        code = 0
        data = message = None
        try:
            data = func(*args, **kwargs)
        except AuthError, e:
            code = e.code
            message = str(e)
            logger.warning(message)
        except BaseError, e:
            code = e.code
            message = str(e)
            logger.warning(message)
        except Exception, e:
            code = 1
            print traceback.format_exc()
            message = str(e)
            logger.error(message)
        res = {'code': code, 'message': message, 'data': data}
        response = HttpResponse(json_dumps(res), content_type='application/json')
        return response


class JumpHandler(BaseHandler):
    def _request_wrapper(self, func, *args, **kwargs):
        try:
            redirect_to = func(*args, **kwargs)
        except AuthError:
            redirect_to = settings.login_url + '?redirect=' + url_quote(self.request.get_raw_uri())
        except Exception, e:
            print traceback.format_exc()
            logger.error(str(e))
            redirect_to = '/403.html'
        return HttpResponseRedirect(redirect_to)


class ViewHandler(BaseHandler):
    def _request_wrapper(self, func, *args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            if isinstance(resp, tuple):
                return render(self.request, resp[0], resp[1], content_type='text/html; charset=utf-8')
            else:
                return render(self.request, resp, content_type='text/html; charset=utf-8')
        except AuthError:
            return HttpResponseRedirect(settings.login_url + '?redirect=' + self.request.get_raw_uri())
        except Exception, e:
            print traceback.format_exc()
            print e
            return HttpResponseRedirect('/403.html')
