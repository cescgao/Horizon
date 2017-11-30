# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Feb 2016


from django.conf.urls import url
from .views import *

patterns = [
    (r'^purify/purify/?$', PurifyPurify),
]

urlpatterns = [url(r[0], r[1].as_view()) for r in patterns]
