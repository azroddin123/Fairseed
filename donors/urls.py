from django.urls import path
from .views import * 
from .views import DonorApi, BankTransactionApi, UpiTransactionApi
import uuid


urlpatterns = [

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



    ###########################################

    # path('donordetail/',DonorDetailApi.as_view()),
    # path('donordetail/<int:pk>',DonorDetailApi.as_view())
    # path('api/recentdonorapi',RecentDonorApi.as_view()),
    path('api/DashboardAPI',DashboardAPI.as_view()),
    
    path('api/DonationsAPApi',DonationsAPApi.as_view()),
    path('api/DashboardDonationsApi',DashboardDonationsApi.as_view()),
    path('api/MyDonationApi/<str:user_id>',MyDonationApi.as_view()),
    path('api/DashboardDonationsViewApi',DashboardDonationsViewApi.as_view()),
    






]


# urlpatterns = [
#     path('donor-details',DonorApi.as_view()),
#     path('donor-details/<str:uuid>',DonorApi.as_view()),


#     path('bank-transaction',BankTransactionApi.as_view()),
#     path('bank-transaction/<str:uuid>',BankTransactionApi.as_view()),


#     path('upi-transaction',UpiTransactionApi.as_view()),
#     path('upi-transaction/<str:uuid>',UpiTransactionApi.as_view())


# ]
