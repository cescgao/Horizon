# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Nov 2017


import requests


class PassportClient(object):

    def __init__(self, host='http://passport.cescgao.top'):
        self.host = host

    def get_info_by_code(self, auth_code):
        url = self.host + '/api/user/info?auth_code=' + auth_code
        req = requests.get(url)
        res = req.json()
        return res['data']
