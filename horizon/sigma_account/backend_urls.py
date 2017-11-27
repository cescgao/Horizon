# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Jan 2016


from django.conf.urls import url
from sigma_account.views import *


patterns = [
    (r'^login/?$', Login),
    (r'^logout/?$', Logout),
]


urlpatterns = [url(r[0], r[1].as_view()) for r in patterns]