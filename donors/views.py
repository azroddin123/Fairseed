from django.shortcuts import render

# Create your views here.
from .serializers import * 
from .models import (
    Donor,
    BankTransaction,
    UpiTransaction
)
from rest_framework.views import APIView
from fairseed.GM1 import GenericMethodsMixin
from rest_framework.response import Response


class DonorApi(GenericMethodsMixin,APIView):
    model = Donor
    serializer_class = DonorSerializer
    lookup_field = "id"

class BankTransactionApi(GenericMethodsMixin,APIView):
    model = BankTransaction
    serializer_class =BankTransactionSerializer
    lookup_field = "id"

class UpiTransactionApi(GenericMethodsMixin,APIView):
    model = UpiTransaction
    serializer_class = UpiSerializers
    lookup_field = "id"


# from django.db.models import Count
# from django.utils import timezone

# current_date = timezone.now()

# # Calculate the date 8 weeks ago
# eight_weeks_ago = current_date - timezone.timedelta(weeks=8)

# # Query to get cumulative donation counts by week number for SQLite
# weekly_donation_counts = Donor.objects.filter(
#     created_at__gte=eight_weeks_ago,
#     created_at__lt=current_date
# ).extra({
#     'week': "strftime('%%W', created_at)",
# }).values('week').annotate(week_count=Count('id')).order_by('week')

# # Calculate cumulative counts
# cumulative_count = 0
# cumulative_counts = []

# for week_count in weekly_donation_counts:
#     cumulative_count += week_count['week_count']
#     cumulative_counts.append({
#         'week': week_count['week'],
#         'cumulative_count': cumulative_count,
#     })

# print("Cumulative Donation Counts:", cumulative_counts)