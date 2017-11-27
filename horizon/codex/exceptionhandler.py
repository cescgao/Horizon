# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Nov 2017


class BaseError(Exception):
    def __init__(self, message):
        self.code = 1
        self.message = message

    def __str__(self):
        return self.message


class AuthError(BaseError):
    def __init__(self, message):
        self.code = 2001
        self.message = message


class OddError(AuthError):
    def __init__(self, message):
        self.code = 2002
        self.message = message


class VerifyError(AuthError):
    def __init__(self, message):
        self.code = 2003
        self.message = message


class ParamsError(BaseError):
    def __init__(self, message):
        self.code = 3001
        self.message = message


class LogicError(BaseError):
    def __init__(self, message):
        self.code = 4001
        self.message = message
