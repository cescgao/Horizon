#-*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Jan 2016


from django.db import models


class Home(models.Model):

    name = models.CharField(max_length=64)
    href_url = models.CharField(max_length=1024)
    pic_url = models.CharField(max_length=1024)
    note = models.TextField()
    available = models.BooleanField(default=1)
    time_create = models.DateTimeField(auto_now_add=True)
    time_modify = models.DateTimeField(auto_now=True)