from django.urls import path
from .views import * 


urlpatterns = [
    path('donor-details',DonorApi.as_view()),
    path('donor-details/<int:pk>',DonorApi.as_view()),


    path('bank-transaction',BankTransactionApi.as_view()),
    path('bank-transaction/<int:pk>',BankTransactionApi.as_view()),


    path('upi-transaction',UpiTransactionApi.as_view()),
    path('upi-transaction/<int:pk>',UpiTransactionApi.as_view())


]
