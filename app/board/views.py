from . import board_blueprint
from flask import request
from ..user.manager import *
from ..models import *


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
        a = Article.query.filter_by(id=args['id']).first()
        return json_status(data=a.base_info)

    @login_required
    def post():
        a = Article(form['title'], form['content'], current_user())
        db.session.add(a)
        db.session.commit()

        return json_status()

    return {
        'GET': get,
        'POST': post
    }[request.method]()
