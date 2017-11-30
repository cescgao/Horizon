# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Jan 2016


from .wrapper import login_required, Passport
from codex import ViewHandler, ApiHandler
from passport import PassportClient
from constants import passport_endpoint


class LoginPage(ViewHandler):

    @login_required
    def get(self):
        return 'account/index.html', {'username': self.request.user['username']}


class Login(ApiHandler):

    def get(self):
        client = PassportClient(passport_endpoint)
        user = client.get_info_by_code(self.input.auth_code)
        Passport.login(self, user)
        return user


class Logout(ApiHandler):

    @login_required
    def post(self):
        Passport.logout(self)

    def get(self):
        return self.post()