from __future__ import absolute_import, unicode_literals
import os

import celery.signals
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_project.settings')


@celery.signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    pass


app = Celery('drf_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
