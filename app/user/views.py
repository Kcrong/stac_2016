from flask import request

from . import user_blueprint
from .manager import *
from ..models import *

from sqlalchemy.exc import IntegrityError


@user_blueprint.route('/account', methods=['GET', 'POST', 'DELETE'])
def account():
    args = request.args
    form = request.form

    def get():
        userid = args.get('userid')
        u = User.query.filter_by(userid=userid).first()
        return json_status(data=u.base_info)

    def post():
        u = User(form['userid'], form['userpw'], form['nickname'])
        db.session.add(u)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            dup = e.args[0].split('failed: ')[1].split('.')[1]
            return json_status(400, status='duplicated', data={'column': dup})
        else:
            return json_status()

    @login_required
    def delete():
        u = current_user()
        db.session.delete(u)
        db.session.commit()
        logout_user()

        return json_status()

    return {
        'GET': get,
        'POST': post,
        'DELETE': delete
    }[request.method]()


@user_blueprint.route('/session', methods=['GET', 'POST', 'PUT', 'DELETE'])
def session():
    form = request.form

    @logout_required
    def post():
        u = User.query.filter_by(userid=form['userid'], userpw=form['userpw']).first()
        if u is None:
            return json_status(401, status='Wrong ID or PW')
        else:
            login_user(u.userid)
            return json_status()

    @login_required
    def delete():
        logout_user()
        return json_status()

    return {
        'POST': post,
        'DELETE': delete
    }[request.method]()
