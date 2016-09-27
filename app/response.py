from flask import jsonify


def json_status(code=200, status='Success', data=None):
    default = {
        'code': code,
        'status': status
    }

    if data is not None:
        default.update(data)

    return jsonify(default), code
