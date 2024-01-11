from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User

def send_otp_via_email(email):
    subject = 'Your Account Verification'
    otp=random.randint(100000, 999999)
    message = f'Your OTP is {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email], fail_silently=False) # fail_silently--> control how the email sending process handles errors
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()

    