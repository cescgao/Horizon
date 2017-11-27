# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Nov 2017


import socket

hostname = socket.gethostname()

if hostname.startswith('vpc-'):
    env = 'prod'
    debug = False

    MASTER_DATABASE_ENGINE = 'django.db.backends.mysql'
    MASTER_DATABASE_NAME = 'horizon'
    MASTER_DATABASE_USER = 'root'
    MASTER_DATABASE_PASSWORD = 'sigmalove'
    MASTER_DATABASE_HOST = '127.0.0.1'
    MASTER_DATABASE_PORT = '3306'

    passport_endpoint = 'http://passport.cescgao.top'

else:
    env = 'dev'
    debug = True

    MASTER_DATABASE_ENGINE = 'django.db.backends.mysql'
    MASTER_DATABASE_NAME = 'horizon'
    MASTER_DATABASE_USER = 'root'
    MASTER_DATABASE_PASSWORD = 'sigmalove'
    MASTER_DATABASE_HOST = '127.0.0.1'
    MASTER_DATABASE_PORT = '3306'

    passport_endpoint = 'http://passport.cescgao.ink'


cookie_expire = 24 * 60 * 60
login_url = passport_endpoint

