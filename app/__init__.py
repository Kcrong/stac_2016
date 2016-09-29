from flask import Flask, session
from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand, Migrate
from flask.ext.sqlalchemy import SQLAlchemy

try:
    import MySQLdb
except ImportError:
    import pymysql
    pymysql.install_as_MySQLdb()

app = Flask(__name__)
db = SQLAlchemy()


def create_app():
    from .main import main_blueprint
    from .user import user_blueprint
    from .board import board_blueprint
    from .files import file_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(board_blueprint, url_prefix='/board')
    app.register_blueprint(file_blueprint, url_prefix='/file')

    app.config.from_pyfile('../config.py')

    return app


app = create_app()

manager = Manager(app)
manager.add_command('db', MigrateCommand)

db.init_app(app)

from .models import *

migrate = Migrate(app, db)


@app.before_first_request
def setting_session():
    session['login'] = False
    session['userid'] = None
