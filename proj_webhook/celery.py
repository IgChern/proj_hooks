from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the environment variable to locate the Django settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj_webhook.settings')

# Create a Celery instance named 'proj_webhook'
app = Celery('proj_webhook')

# Configure Celery using the settings from the Django configuration
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover and register tasks within the Celery app
app.autodiscover_tasks(['app_hooks.tasks'])
