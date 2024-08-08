
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Campaign
from fairseed.task import send_email_fun
from portals.services import campaign_creation_updation
from fairseed.settings import EMAIL_HOST_USER

@receiver(post_save, sender=Campaign)
def send_email_on_model_creation_or_update(sender, instance, created, **kwargs):
    if created:
        subject = "Fairseed Campaign Creation Mail"
        message = f"Your campaign '{instance.title}' has been created, and a request for approval has been sent to the admin."
        send_email_fun.delay(subject, message, EMAIL_HOST_USER, instance.user.email)
        # campaign_creation_updation(instance.user.email,instance.status,instance.title,subject,message)
    else:
        subject = "Fairseed Campaign Updation Mail"
        message = "Your Campaign Data is Updated Now"
        send_email_fun.delay(subject, message, EMAIL_HOST_USER, instance.user.email)
        # campaign_creation_updation(instance.email,instance.status,instance.title,subject,message)