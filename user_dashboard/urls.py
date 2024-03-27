from django.urls import path
from .views import * 
from accounts.views import ChangePasswordApi


urlpatterns = [
    # Get all User Campaign api
    path('campaign',CampaignApi3.as_view()),
    path('campaign/<str:pk>',CampaignApi3.as_view()),
    path('cause-edit/<str:pk>',CauseEditAPi.as_view()),
    # Get Approved Donation 
    path('my-donations',MyDonationApi.as_view()),
    path('my-donations/<str:pk>',MyDonationApi.as_view()),
    
    #Get Bank And Kyc Details 
    path("bank-kyc",BankKycApi.as_view()),
    path("bank-kyc/<str:pk>",BankKycApi.as_view()),
    # Edit bank and kyc API
    path('edit-bankkyc/<str:pk>',ViewBankAndKycAPi.as_view()),
    path('edit-bankkyc/<str:pk>',ViewBankAndKycAPi.as_view()),
    
    path('donations',ReceivedDonationApi.as_view()),
    path('donations/<str:pk>',ReceivedDonationApi.as_view()),
    path('dashboard-api',UserDashboardApi.as_view()),
    
    path("donation-data",DonationCountApi.as_view()),
    
    path('fundraiser-data',FundRaisedApi.as_view())

]