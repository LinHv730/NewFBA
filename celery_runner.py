# -*- coding: utf-8 -*-
import os
from app import create_app
from celery import Celery 
from config import config
from app.tasks import getIrobotboxorder
###由flask传入的app绑定celery
def make_celery(app):
  celery = Celery(
    app.import_name,
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND']
    )

  celery.conf.update(app.config)
  Taskbase=celery.Task 

  class ContextTask(Taskbase):
    abstract=True

    def __call__(self,*args,**kwargs):
      with app.app_context():
        return Taskbase.__call__(self,*args,**kwargs)

  celery.Task=ContextTask
  return celery

env=os.environ.get('WEBAPP_ENV','Pro') ###为什么不写全称是因为后面有拼接
flask_app=create_app('default')
  # 'app.config.%sConfig' %env.capitalize()
celery=make_celery(flask_app)