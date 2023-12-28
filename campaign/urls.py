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

##################################################################

    path('api/CampaignGetApi', CampaignGetApi.as_view()),
    path('api/CampaignCatagoriesGetApi', CampaignCatagoriesGetApi.as_view()),

    path('api/CampaignRaisedUserApi', CampaignRaisedUserApi.as_view()),
    # path('api/CampaignDetailApi', CampaignDetailApi.as_view()),
    # path('api/SuccessfulCampaignCount', SuccessfulCampaignCount.as_view()),
    # path('api/success_cam', success_cam.as_view()),

    path('api/CampaignCatagoriesListAPI',CampaignCatagoriesListAPI.as_view()),

    path('api/StdBenefitedCountAPI', StdBenefitedCountAPI.as_view()),
    path('api/SuccessCount', SuccessCount.as_view()),
    path('api/CampaignCategoryCausesAPI/<int:pk>', CampaignCategoryCausesAPI.as_view()),
    path('api/CapmPaginationApi', CapmPaginationApi.as_view()),
    
    
    
    # path('api/campaign/<int:pk>/', success_fund.as_view(), name='campaign_detail'),
    # path('api/updatecamstatus/<int:pk>',update_cam_status, name=update_cam_status),

    
]
