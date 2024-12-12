from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module for 'celery'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "health.settings.base")

app = Celery("health")

# Using a string here means the worker doesn't need to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send-scheduled-email': {
        'task': 'your_app.tasks.send_scheduled_email',
        'schedule': crontab(minute=0, hour=9),  # This will run daily at 9:00 AM
        'args': ("Scheduled Email", "This is a scheduled test email.", ['recipient@example.com']),
    },
}

# Autodiscover tasks in installed apps
app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True
