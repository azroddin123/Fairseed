from django.urls import path
from .views import * 

urlpatterns = [
    ###################################################################################################
    path('api/categories/', CategoriesApi.as_view(),name='categories'),
    path('api/description/<str:pk>/', CampaignDescriptionApi.as_view(), name='campaign-description-api'),
    path('api/causesbycategory/', Causes_by_CategoryAPI.as_view(),name='cause_categories'),
    path('api/card/', CardAPI.as_view(), name='cardview'),
    path('api/practice/', PracticeAPI.as_view()),
    path('api/causes_raised/', TotalCountAPI.as_view(), name='causes-raised'),
    # path('api/landing_page/card/', CardAPIViewPagination.as_view()),
    path('api/admin/dashboard/', DashboardAPI.as_view(), name='dashboard-api'),
    # path('api/landing_page/causes_by_category',CausesbyCategoryAPI.as_view()),
    # path('api/landing_page/ongoing_campaign_built_in/',Ongoing_Campaign_Api_built_in.as_view()),
    # path('api/landing_page/ongoing_campaign/',Ongoing_Campaign_Api.as_view()),
    ###################################################################################################
    
    path('campaign-category',CampaigncategoryApi.as_view()),
    path('campaign-category/<str:pk>',CampaigncategoryApi.as_view()),

    path('campaign-details',CKBApi.as_view()),
    path('campaign-details/<str:pk>',CKBApi.as_view()),

    # path('kyc-details',KycApi.as_view()),
    # path('kyc-details/<str:pk>',KycApi.as_view()),

    path('documents',DocumentApi.as_view()),
    path('documents/<str:pk>',DocumentApi.as_view()),


    path('landing-page',LandingPageApi.as_view()),
    path('campaign-filter',CampaignFilterApi.as_view()),
    path('campaign/<str:pk>', CampaignDetailsApi.as_view()),
    path('campaign', CampaignDetailsApi.as_view()),
    path('catagory', CampaignByCategoryApi.as_view()),
    

    # path('campaign/<str:pk>/', CampaignDetailsApi.as_view(), name='campaign-details'),
    # path('campaign/', CampaignDetailsApi.as_view(), name='campaign-list'),
    # path('category/', CampaignByCategoryApi.as_view(), name='campaign-by-category'),
]