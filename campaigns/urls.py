from django.urls import path
from .views import * 

urlpatterns = [

  
    
    path('campaign-category',CampaigncategoryApi.as_view()),
    path('campaign-category/<str:pk>',CampaigncategoryApi.as_view()),

    # path('campaign-details',CKBApi.as_view()),
    # path('campaign-details/<str:pk>',CKBApi.as_view()),

    # path('kyc-details',KycApi.as_view()),
    # path('kyc-details/<str:pk>',KycApi.as_view()),

    path('documents',DocumentApi.as_view()),
    path('documents/<str:pk>',DocumentApi.as_view()),


    path('landing-page',LandingPageApi.as_view()),
    path('campaign-filter',CampaignFilterApi.as_view()),
    path('campaign/<str:pk>', CampaignApi.as_view()),
    path('campaign', CampaignApi.as_view()),
    path('catagory', CampaignByCategoryApi.as_view()),
    path('campaign-details/<str:pk>', CampaignDetailsApi.as_view())

    # path('campaign/<str:pk>/', CampaignDetailsApi.as_view(), name='campaign-details'),
    # path('campaign/', CampaignDetailsApi.as_view(), name='campaign-list'),
    # path('category/', CampaignByCategoryApi.as_view(), name='campaign-by-category'),
]