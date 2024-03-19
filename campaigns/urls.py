from django.urls import path
from .views import * 

urlpatterns = [
    path('campaign-category',CampaigncategoryApi.as_view()),
    path('campaign-category/<str:pk>',CampaigncategoryApi.as_view()),
    
    path('documents',DocumentApi.as_view()),
    path('documents/<str:pk>',DocumentApi.as_view()),
    
    # Logical API List 
    path('landing-page',LandingPageApi.as_view()),
    path('campaign-filter',CampaignTabsAPi.as_view()),
    path('campaign/<str:pk>', CampaignApi.as_view()),
    path('campaign', CampaignApi.as_view()),
    
    # Campaign By Category 
    path('category',CampaignFilterApi.as_view()),
    path('category', CampaignByCategoryApi.as_view()),
    path('category/<str:pk>',CampaignByCategoryApi2.as_view()),
    path('campaign-details/<str:pk>', CampaignDetailsApi.as_view()),
   
    # add campaign
    path('add-campaign/<str:pk>',AddCampaignApi.as_view()),
    path('add-campaign',AddCampaignApi.as_view()),
    
    # Donation API
    # bank And Kyc 
    
]