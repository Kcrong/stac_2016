from . import file_blueprint
from flask import request, send_file
from ..user.manager import *
from ..models import *


@file_blueprint.route('/image', methods=['GET', 'POST'])
def image():
    profile_image = request.files['file']
    form = request.form

    def get():
        image = User.query.filter_by(userid=form['userid']).first().image
        return send_file('../static/' + image)

    @login_required
    def post():
        u = current_user()
        u.add_profile(profile_image)
        db.session.commit()

        return json_status()

    return {
        'GET': get,
        'POST': post
    }[request.method]()
