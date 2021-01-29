import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Секретный ключ
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'n]y-s6P+q\y*}QN(CGz"xBZFo]gZ[GZ8'
    # Подключение к БД
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Почта
    MAIL_SERVER = '' #os.environ.get('MAIL_SERVER')
    MAIL_PORT = 465 #int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = False #os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'u' #os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = '' #os.environ.get('MAIL_PASSWORD')
    ADMINS = ['']

    POSTS_PER_PAGE = 30