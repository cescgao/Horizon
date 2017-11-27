# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Nov 2017


from django.db import models
from django_mysql.models.fields.json import JSONField


class ObjAccessToken(models.Model):
    uid = models.CharField(max_length=16, db_index=True)
    access_token = models.CharField(max_length=64, db_index=True, unique=True)
    data = JSONField()
    expire = models.DateTimeField()
    time_create = models.DateTimeField(auto_now_add=True)
