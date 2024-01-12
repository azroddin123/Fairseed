from django.urls import path
from .views import * 
from accounts.views import ChangePasswordApi


urlpatterns = [
    
    path('campaign',CampaignApi.as_view()),
    path('my-campaign/<str:pk>',CampaignApi.as_view()),
    
    
    path('my-donations',MyDonationApi.as_view()),
    path('my-donations/<str:pk>',MyDonationApi.as_view()),

    path('dashboard-api',UserDashboardApi.as_view()),
    
    path("donation-data",DonationCountApi.as_view()),
    
    path('fundraise-data',FundRaisedApi.as_view())

]