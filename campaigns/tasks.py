# campaigns/tasks.py
#for scheduling campaign expire
from celery import shared_task
from .models import Campaign

from django.utils import timezone

@shared_task
def update_campaign_statuses():
    today = timezone.now().date()
    campaigns=Campaign.objects.all()
    objects_to_update = [campaign for campaign in campaigns if campaign.days_left <= 0]
    
    for obj in objects_to_update:
        print("Im here")
        if obj.days_left == 0 and obj.status != 'Completed':
            obj.status = 'Completed'
            obj.save(update_fields=['status'])
