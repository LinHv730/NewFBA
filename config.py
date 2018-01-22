# -*- coding:utf-8 -*-
from datetime import timedelta

class Config(object):
    SECRET_KEY = "Ay98Cct2oNSlnHDdTl8"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class LastConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/new_test"
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERYBEAT_SCHEDULE = {
        'getIrobotboxorder_every_15':{
            'task':'app.tasks.getIrobotboxorder',
            "schedule": timedelta(seconds=30),
        },
        'getAgain_every_15':{
            'task':'app.tasks.getdataAgain',
            "schedule": timedelta(seconds=60),
        }
    }


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/test_data"


config = {'default':LastConfig, 'test':TestConfig}