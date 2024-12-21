import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_every_monday_8am': {
        'task': 'news.tasks.weekly_update',
        'schedule': crontab(minute='0', hour='8', day_of_week='monday'),
    },
}

app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'news.tasks.weekly_update',
        'schedule': 20,
    },
}
