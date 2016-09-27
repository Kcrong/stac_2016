from flask import session
from ..response import json_status
from ..models import User


def login_required(func):
    def check_login(*args, **kwargs):
        try:
            session['login']
        except KeyError:
            session['login'] = False
        finally:
            if session['login'] is True:
                return func(*args, **kwargs)
            else:
                return json_status(401, "Login Required")

    return check_login


def logout_required(func):
    def check_logout(*args, **kwargs):
        try:
            session['login']
        except KeyError:
            session['login'] = False
        finally:
            if session['login'] is False:
                return func(*args, **kwargs)
            else:
                return json_status(401, "Login Required")

    return check_logout


def login_user(userid):
    session['login'] = True
    session['userid'] = userid


def logout_user():
    session['login'] = False
    session['userid'] = None


def current_user():
    u = User.query.filter_by(userid=session['userid']).first()
    return u
