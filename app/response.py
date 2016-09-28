from flask import jsonify


def json_status(code=200, status=None, data=None):
    if status is not None:
        pass
    elif code == 200:
        status = 'Success'
    else:
        status = 'Failed'

    default = {
        'code': code,
        'status': status
    }

    if data is not None:
        default.update(data)

    return jsonify(default), code
