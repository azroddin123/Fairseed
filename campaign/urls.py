from django.urls import path
from .views import * 

urlpatterns = [

    path('cause',CampaignApi.as_view()),
    path('cause/<int:pk>',CampaignApi.as_view()),
    
    path('campaign-catagory',CampaignCatagoryApi.as_view()),
    path('campaign-catagory/<int:pk>',CampaignCatagoryApi.as_view()),

    path('bank-details',BBDApi.as_view()),
    path('bank-details/<int:pk>',BBDApi.as_view()),

    path('kyc-details',KycApi.as_view()),
    path('kyc-details/<int:pk>',KycApi.as_view()),

    path('dashboard-api',DashboardApi.as_view()),
    path('campaign-filter',CampaignFilterApi.as_view())
]