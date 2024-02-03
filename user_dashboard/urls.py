from django.urls import path
from .views import * 
from accounts.views import ChangePasswordApi


urlpatterns = [
    # Get all User Campaign api
    path('campaign',CampaignApi.as_view()),
    path('my-campaign/<str:pk>',CampaignApi.as_view()),
    
    # Get Approved Donation 
    path('my-donations',MyDonationApi.as_view()),
    path('my-donations/<str:pk>',MyDonationApi.as_view()),
    
    #Get Bank And Kyc Details 
    
    # path("bank-kyc",BankKycApi.as_view()),
    
    # Get Receieved Donation 
    path('donations',RecivedDonationApi.as_view()),

    path('dashboard-api',UserDashboardApi.as_view()),
    
    path("donation-data",DonationCountApi.as_view()),
    
    path('fundraise-data',FundRaisedApi.as_view())

]