from . import file_blueprint
from flask import request
from ..user.manager import *
from ..models import *


@file_blueprint.route('/image', methods=['GET', 'POST'])
def comment():
    form = request.form

    @login_required
    def post():
        return json_status()

    return {
        'POST': post
    }[request.method]()
