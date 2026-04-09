
import os
import sys
from celery import Celery
from datetime import datetime, timedelta


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# initialise celery
celery_app = Celery(
    'hms_tasks',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
    include=['tasks']
)

# config celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  
    result_expires=3600,  
)

# beat scedule 
try:
    from celery_beat_conf import CELERY_BEAT_SCHEDULE, CELERY_TASK_ROUTES, CELERY_CONFIG
    celery_app.conf.beat_schedule = CELERY_BEAT_SCHEDULE
    celery_app.conf.task_routes = CELERY_TASK_ROUTES
    celery_app.conf.update(CELERY_CONFIG)
except ImportError:
    pass

def make_celery(app=None):
    
    if app:
        class ContextTask(celery_app.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        
        celery_app.Task = ContextTask
    return celery_app


if __name__ == '__main__':
    celery_app.start()
