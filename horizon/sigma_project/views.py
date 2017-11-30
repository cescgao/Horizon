# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Feb 2016


from codex import ViewHandler, ApiHandler
from sigma_account.wrapper import login_required
import requests


class ProjectPage(ViewHandler):
    @classmethod
    def get(cls):
        return 'project/index.html'


class PurifyPage(ViewHandler):
    @login_required
    def get(self):
        return 'project/purify.html'


class PurifyPurify(ApiHandler):
    @login_required
    def post(self):
        return requests.post('http://127.0.0.1:5001/v1/purify', data={'url': self.input.url}).json()
