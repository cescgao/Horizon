# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Jan 2016


from codex import ViewHandler


class HomePage(ViewHandler):

    @classmethod
    def get(cls):
        return 'home/index.html'
