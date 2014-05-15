import os
    _basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = False

    ADMINS = frozenset(['youremail@yourdomain.com'])
    SECRET_KEY = 'This string will be replaced with a proper key in production.'

    #  Just an in-memory database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DATABASE_CONNECT_OPTIONS = {}

    THREADS_PER_PAGE = 8
