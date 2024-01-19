from django.urls import path
from .views import *
from .views import DonorApi, BankTransactionApi, UpiTransactionApi
import uuid


urlpatterns = [

#########################################################################
    path('api/donor_record/',DonorRecord.as_view()),
#########################################################################
    path('donor-details', DonorApi.as_view()),
    path('donor-details/<int:pk>', DonorApi.as_view()),

    path('bank-details', BankTransactionApi.as_view()),
    path('bank-details/<int:pk>', BankTransactionApi.as_view()),

    path('upi-transaction', UpiTransactionApi.as_view()),
    path('upi-transaction/<int:pk>', UpiTransactionApi.as_view()),
    
    ##################################################################

    path('donor-details',DonorApi.as_view()),
    path('donor-details/<str:uuid>',DonorApi.as_view()),


    path('bank-transaction',BankTransactionApi.as_view()),
    path('bank-transaction/<str:uuid>',BankTransactionApi.as_view()),


    path('upi-transaction',UpiTransactionApi.as_view()),
    path('upi-transaction/<str:uuid>',UpiTransactionApi.as_view()),


# urlpatterns = [
#     path('donor-details',DonorApi.as_view()),
#     path('donor-details/<str:uuid>',DonorApi.as_view()),


#     path('bank-transaction',BankTransactionApi.as_view()),
#     path('bank-transaction/<str:uuid>',BankTransactionApi.as_view()),


#     path('upi-transaction',UpiTransactionApi.as_view()),
#     path('upi-transaction/<str:uuid>',UpiTransactionApi.as_view())


# ]

#################################################################################################################################################
    path('api/donor-form/',DonateToCampaign.as_view()), # Donate To Campaign Page
    path('api/donate_to_bank_transfer/',DonateToBankTransfer.as_view()), # Donate To Bank Transfer
    path('api/donate_to_bank_transfer/<str:pk>/',DonateToBankTransfer.as_view()), # Donate To Bank Transfer
    # path('api/donate_bank_transaction/', BankTransaction1.as_view()),
#################################################################################################################################################
]