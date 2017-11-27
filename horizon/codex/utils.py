# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Nov 2017


import uuid
import datetime
import time
import base64
import hashlib
import ujson
import urllib
import urlparse
import platform
import subprocess
import os


def json_dumps(data):
    return ujson.dumps(data, double_precision=4)


def json_loads(data):
    return ujson.loads(data)


def generate_hash_limit(limit=None):
    hash_string = uuid.uuid4().hex
    if limit:
        return hash_string[: limit]
    return hash_string


def get_datetime_now():
    return datetime.datetime.now()


def get_datetime_utcnow():
    return datetime.datetime.utcnow()


def get_timestamp_now():
    return time.time()


def strptime(t, f='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(t, f)


def strftime(t, f='%Y-%m-%d %H:%M:%S'):
    return t.strftime(f)


def from_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def to_timestamp(t):
    return time.mktime(t.timetuple())


def sha1(string):
    return hashlib.sha1(string).hexdigest()


def md5(string):
    return hashlib.md5(string).hexdigest()


def b64encode(string):
    return base64.b64encode(string)


def b64decode(string):
    return base64.b64decode(string)


def timedelta(**kwargs):
    return datetime.timedelta(**kwargs)


def pipe(cls, args):
    if platform.system() == 'Windows':
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out
    else:
        p = os.popen(args)
        return p.read()


def url_parser(url):
    return urlparse.urlparse(url)


def url_encoder(data):
    return urllib.urlencode(data)


def url_quote(url):
    return urllib.quote(url)


def url_unquote(url):
    return urllib.unquote(url)


class Dict(dict):
    def __getattr__(self, item):
        resp = self.get(item, None)
        if isinstance(resp, dict):
            resp = Dict(resp)
            # resp.__duplicated__ = True
        return resp

    def __setattr__(self, key, value):
        self[key] = value
