# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Jan 2016


from django.conf.urls import url
from .views import *


patterns = [
]


urlpatterns = [url(r[0], r[1].as_view()) for r in patterns]