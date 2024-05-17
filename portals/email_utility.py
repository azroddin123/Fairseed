# email_utils.py
import threading
from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )

class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        send_email(self.subject, self.message, self.recipient_list)

def send_email_async(subject, message, recipient_list):
    EmailThread(subject, message, recipient_list).start()
