import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_APP='Intervals_analyzer.py'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' #todo ensure env variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
