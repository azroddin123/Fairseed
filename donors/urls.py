from django.urls import path
from .views import * 
from .phone_pay import *
import uuid


urlpatterns = [
    path('donor-details',DonorApi.as_view()),
    path('donor-details/<str:uuid>',DonorApi.as_view()),
    
    # path('donate',pay,name="pay"),
    path('money',PayApi.as_view()),
    path('bank-transaction',BankTransactionApi.as_view()),
    path('bank-transaction/<str:uuid>',BankTransactionApi.as_view()),

    path('upi-transaction',UpiTransactionApi.as_view()),
    path('upi-transaction/<str:uuid>',UpiTransactionApi.as_view())

]


# urlpatterns = [
#     path('donor-details',DonorApi.as_view()),
#     path('donor-details/<str:uuid>',DonorApi.as_view()),


#     path('bank-transaction',BankTransactionApi.as_view()),
#     path('bank-transaction/<str:uuid>',BankTransactionApi.as_view()),


#     path('upi-transaction',UpiTransactionApi.as_view()),
#     path('upi-transaction/<str:uuid>',UpiTransactionApi.as_view())


# ]
