
from celery import shared_task
from django.core.mail import send_mail
import time

@shared_task(serializer='json', name="send_mail")
def send_email_fun(subject, message, sender, receiver):
    time.sleep(10) 
    send_mail(subject, message, sender, [receiver],fail_silently=True)