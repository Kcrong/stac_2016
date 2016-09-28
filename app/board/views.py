from . import board_blueprint
from flask import request
from ..user.manager import *


@board_blueprint.route('/comment', methods=['GET', 'POST'])
def comment():
    form = request.form

    @login_required
    def post():
        pass

    return {
        'POST': post
    }[request.method]()


@board_blueprint.route('/article', methods=['GET', 'POST'])
def article():
    args = request.args
    form = request.form

    def get():
        pass

    def post():
        pass

    return {
        'GET': get,
        'POST': post
    }[request.method]()
