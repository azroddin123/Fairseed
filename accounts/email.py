from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User
from datetime import datetime, timedelta

def send_otp_via_email(email):
    subject = 'Your Account Verification'
    otp=random.randint(1000, 9999)
    message = f'Your OTP is {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email], fail_silently=False)
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()

# def send_otp_via_email_forgot_password(email):
#     otp = random.randint(100000, 999999)
#     subject = 'Your OTP for Account Verification'
#     message = f'Your OTP is {otp}. Please use this OTP to verify your account.'
#     email_from = settings.EMAIL_HOST

#     send_mail(subject, message, email_from, [email], fail_silently=False)
#     user_obj = User.objects.get(email=email)
#     user_obj.otp = otp
#     user_obj.save()

#     return otp

# def verify_otp(email, entered_otp):
#     try:
#         user = User.objects.get(email=email)

#         if user.otp == entered_otp:
#             # Check if the OTP is still valid (e.g., within a time window)
#             otp_generated_time = user.otp_generated_time
#             current_time = datetime.now()
#             time_difference = current_time - otp_generated_time

#             # Assuming OTP is valid for 5 minutes (adjust as per your requirement)
#             if time_difference.total_seconds() <= 300:
#                 return True
#             else:
#                 return False
#         else:
#             return False

#     except User.DoesNotExist:
#         return False