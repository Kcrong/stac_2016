from . import board_blueprint


@board_blueprint.route('/comment', methods=['GET', 'POST'])
def comment():
    return "Hello I am Server~"
