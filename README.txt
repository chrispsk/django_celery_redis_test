# django_celery_redis_test
Blank project! Implementing Celery and Redis. Tasks, Periodic Tasks, Deployment to Heroku

Locally After All:
[
Start Redis server
Start celery: celery -A setari worker -l info
Start simple beat: celery -A setari beat -l info
Start database beat: celery -A setari beat -S django
]


start the server redis

1) In virtual env: 
pip install celery
pip install redis
pip install django-celery-beat
pip install django-celery-results
pip freeze > requirements.txt

2) In settings.py: 

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_celery_results',
]


# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_BROKER_URL = os.environ['REDIS_URL']
CELERY_RESULT_BACKEND = os.environ['REDIS_URL']
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

3) In mainapp(setari) create celery.py:

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# for windows add this:
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

# set the default Django settings module for the 'celery' program.
# like in .wsgi
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setari.settings')


app = Celery('proj')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

4) In __init__.py inside setari:
from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app  # noqa

5) python manage.py startapp billing
Create model for Billing
    item_name = models.CharField(max_length=120)
    number_1 = models.IntegerField()
    number_2 = models.IntegerField()
    total = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{total}".format(total=self.total)

6) Inside billing create tasks.py:

from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task
# can use database
# from billing.models import Billing

@task(name="sum_two_numbers")
def add(x, y):
    return x + y


@task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    Billing.objects.create(etc. etc. etc.) ### can use database
    return total


@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)

7) python manage.py makemigrations / migrate
8) from virtual environment src:
celery -A setari worker -l info
9) python manage.py shell :
>>>from billing.tasks import add, mul, xsum

# normal operations
>>> add(123,30)

153

>>> mul(323,23)

64632

>>> xsum([123,423])


546

# with celery
>>> add.delay(12,30)


######################## SHEDULE TASKS ###################
In celery.py:
from celery.schedules import crontab

Before app.autodiscover_tasks() add: 

app.conf.beat_schedule = {
    'add-every-minute-contrab': {
        'task': 'multiply_two_numbers',
        'schedule': crontab(),
        'args': (16, 16),
    },
    'add-every-5-seconds': {
        'task': 'multiply_two_numbers',
        'schedule': 5.0,
        'args': (16, 16)
    },
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}


>>> celery -A setari worker -l info
>>> celery -A setari beat -l info
OR by database schedule use:
>>> celery -A setari beat -l info -S django (foloseste pe amandoua. cele din database si cele din tasks.py)

###################### DEPLOY ON HEROKU #####################
1) .gitignore (get rid of local environ but create requirements.txt instead)
2) same level as manage.py CREATE Procfile:
In Procfile:
web: gunicorn setari.wsgi --log-file -
worker: celery -A setari worker

#For database
#beat: celery -A setari beat -S django
#OR simple beat: celery -A setari beat -l info

3) pip install django psycopg2 dj-database-url gunicorn
4) git init
5) git add .
6) git commit -m "First Init"
7) heroku create chrishop
8.1) heroku addons:create heroku-postgresql:hobby-dev
8.2) install redis ~ heroku addons:create heroku-redis:hobby-dev
9) in settings.py under database: (will override the settings to use postgresql database)
import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500

10) git add .
11) git commit -m "change database"

12) heroku config:set DISABLE_COLLECTSTATIC=1

13.1) git push heroku master
13.2) After pushing: SCALE:
~ heroku ps:scale web=1 worker=1
OR if using schedule
~ heroku ps:scale web=1 worker=1 beat=1 (must be paid plan)

14) heroku run python manage.py migrate
15) heroku run bash
16) python manage.py createsuperuser
17) heroku open


heroku restart

Special in view:
def home(request):
    total = abcsum.delay([2,9])
    # time.sleep(1)
    return HttpResponse(total.get()) # get() to return from Queue when finishes

