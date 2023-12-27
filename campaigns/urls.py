from django.urls import path
from .views import * 

urlpatterns = [

    path('cause',CampaignDetailsApi.as_view()),
    path('cause/<str:pk>',CampaignDetailsApi.as_view()),
    
    path('campaign-category',CampaigncategoryApi.as_view()),
    path('campaign-category/<str:pk>',CampaigncategoryApi.as_view()),

    path('campaign-details',CKBApi.as_view()),
    path('campaign-details/<str:pk>',CKBApi.as_view()),

    # path('kyc-details',KycApi.as_view()),
    # path('kyc-details/<str:pk>',KycApi.as_view()),

    path('documents',DocumentApi.as_view()),
    path('documents/<str:pk>',DocumentApi.as_view()),


    path('dashboard-api',DashboardApi.as_view()),
    path('campaign-filter',CampaignFilterApi.as_view()),

    path('category_filter/<str:pk>',CampaignBycategoryApi.as_view())
]