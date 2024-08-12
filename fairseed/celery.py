import os
from celery import Celery

from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fairseed.settings')

app = Celery('fairseed')

# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

#Scheduling the task
app.conf.beat_schedule={
    'Update status daily':{
        'task':'campaigns.tasks.update_campaign_statuses',
        'schedule':crontab(hour=0,minute=0),
    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()