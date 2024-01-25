from django.urls import path
from .views import * 

urlpatterns = [
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

    #################################################################

    path('api/CampaignGetApi', CampaignGetApi.as_view()),
    path('api/CampaignPostApi', CampaignPostApi.as_view()),

    path('api/CampaignDetailPostApi', CampaignDetailPostApi.as_view()),

    path('api/CreateCampaignStep1', CreateCampaignStep1.as_view()),

    # path('api/CreateCampaignStep3', CreateCampaignStep3.as_view()),
    path('api/CreateCampaignStep3/<str:campaign_id>/', CreateCampaignStep3.as_view()),
    
    path('api/CreateCampaignStep2', CreateCampaignStep2.as_view()),
    path('api/CreateCampaignStep2/<str:campaign_id>/', CreateCampaignStep2.as_view()),

    path('api/CreateCampaignStep4/', CreateCampaignStep4.as_view()),
    path('api/CreateCampaignStep4/<str:campaign_id>/', CreateCampaignStep4.as_view()),

    path('api/CampaignDetailStoryApi', CampaignDetailStoryApi.as_view()),
    
    path('api/CampaignCreateApi1', CampaignCreateApi1.as_view()),
    
    path('api/CampaignDeletePutApi/<int:pk>', CampaignDeletePutApi.as_view()),
    
    path('api/CampaignCatagoriesGetApi', CampaignCatagoriesGetApi.as_view()),

    path('api/CampaignRaisedUserApi', CampaignRaisedUserApi.as_view()),
    path('api/CampaignDetailApi', CampaignDetailApi.as_view()),
    # path('api/SuccessfulCampaignCount', SuccessfulCampaignCount.as_view()),

    path('api/CampaignCatagoriesListAPI',CampaignCatagoriesListAPI.as_view()),
    path('api/CamapaignActionApi/<str:id>',CamapaignActionApi.as_view()),
    path('api/CamapaignActionApi1/',CampaignCatagoriesGetApi1.as_view()),
    
    

    path('api/StdBenefitedCountAPI', StdBenefitedCountAPI.as_view()),
    path('api/SuccessCount', SuccessCount.as_view()),
    path('api/CampaignCategoryCausesAPI/<int:pk>', CampaignCategoryCausesAPI.as_view()),
    path('api/CapmPaginationApi/<int:pk>/', CapmPaginationApi.as_view()),
    
    path('CampaignCause/<int:pk>', CampaignCause1.as_view()),
    path('api/camapaigncause', CamapaignCauseApi.as_view()),

    path('api/CardAPIViewPagination', CardAPIViewPagination.as_view()),
    path('api/landing_page/card/', CardAPIViewPagination.as_view()),

    path('api/OneCardApi', OneCardApi.as_view()),
    path('api/RecentDonorApi/<str:camp_id>', RecentDonorApi.as_view()),

    path('api/practice', practice.as_view()),

    path('api/campaignsearch/', CampaignSearchApi.as_view()),

    path('api/scholarshipcampaign/', ScholarshipCampaignApi.as_view()),
    
    path('api/RelegiousEducationCampApi', RelegiousEducationCampApi.as_view()),

    path('api/ReportedCampaignApi', ReportedCampaignApi.as_view()),

    path('api/admin/campaign/', CampaignAdminApi.as_view()),


]