import debug
import random
import string

if debug.DEBUG:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
else:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@localhost:3306/stac_2016?charset=utf8'


def randomkey(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


SECRET_KEY = 'development-key'
SQLALCHEMY_TRACK_MODIFICATIONS = True
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
TRAP_BAD_REQUEST_ERRORS = True
SQLALCHEMY_POOL_RECYCLE = 3600
