import logging
import os

class BaseConfig:
    LOGGING_LEVEL = logging.INFO

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gotit1234'

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1/catalog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ITEMS_PER_PAGE = 10
    CATEGORIES_PER_PAGE = 5
