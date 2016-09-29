from . import file_blueprint
from flask import request, send_file
from ..user.manager import *
from ..models import *
from config import PROFILE_IMAGE_PATH


@file_blueprint.route('/image', methods=['GET', 'POST'])
def image():
    args = request.args
    form = request.form

    def get():
        image = User.query.filter_by(userid=args['userid']).first().image
        return send_file(os.path.join(PROFILE_IMAGE_PATH, image))

    @login_required
    def post():
        profile_image = request.files['file']
        u = current_user()
        u.add_profile(profile_image)
        db.session.commit()

        return json_status(data={'image': u.image})

    return {
        'GET': get,
        'POST': post
    }[request.method]()
