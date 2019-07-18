from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
# like in .wsgi
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setari.settings')

app = Celery('proj')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

############## FOR BEAT (Periodic Tasks, RAW OR DATABASE) ##############

# app.conf.beat_schedule = {
#     'add-every-minute-contrab': {
#         'task': 'multiply_two_numbers',
#         # 'schedule': crontab(hour=7, minute=30, day_of_week=1), # Every monday morning at 7:30
#         'schedule': crontab(), # by default every minute
#         'args': (16, 16),
#     },
#     'add-every-5-seconds': {
#         'task': 'multiply_two_numbers',
#         'schedule': 5.0, # in seconds
#         'args': (16, 16)
#     },
#     'add-every-monday-morning': {
#         'task': 'billing.tasks.abcsum',
#         'schedule': crontab(hour=8, day_of_week=1),
#         'args': (16, 16)
#     },
#
#     # 'add-every-30-seconds': {
#     #     'task': 'tasks.add',
#     #     'schedule': 30.0,
#     #     'args': (16, 16)
#     # },
# }
########################## END BEAT ###################################
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
