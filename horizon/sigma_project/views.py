# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Feb 2016


from codex import ViewHandler


class ProjectPage(ViewHandler):

    @classmethod
    def get(cls):
        return 'project/index.html'
