from django.urls import path

from .views import *

urlpatterns = [

    ###################################################################################################
    # path('card/', CardAPIView.as_view()),
    path('api/landing_page/card/', CardAPIViewPagination.as_view()),
    path('api/admin/dashboard/', DashboardAPI.as_view(), name='dashboard-api'),
    # path('api/landing_page/causes_by_category',CausesbyCategoryAPI.as_view()),
    # path('api/landing_page/ongoing_campaign_built_in/',Ongoing_Campaign_Api_built_in.as_view()),
    # path('api/landing_page/ongoing_campaign/',Ongoing_Campaign_Api.as_view()),
    ###################################################################################################

    path('cause',CampaignApi.as_view()),
    path('cause/<int:pk>',CampaignApi.as_view()),

    path('campaign/',CampaignView.as_view()),
    path('campaign_categories/',CampaignCatagoriesView.as_view()),

    path('campaign-catagory',CampaignCatagoryApi.as_view()),
    path('campaign-catagory/<int:pk>',CampaignCatagoryApi.as_view()),

    path('bank-details',BBDApi.as_view()),
    path('bank-details/<int:pk>',BBDApi.as_view()),

    path('kyc-details',KycApi.as_view()),
    path('kyc-details/<int:pk>',KycApi.as_view())
]