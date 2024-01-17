'''
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj_webhook.settings')

app = Celery('proj_webhook')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
'''
