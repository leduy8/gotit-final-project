import logging
import os
from werkzeug.security import generate_password_hash, check_password_hash

class BaseConfig:
    LOGGING_LEVEL = logging.INFO

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gotit1234'

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1/catalog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ITEMS_PER_PAGE = 10
