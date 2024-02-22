from django.urls import path
from .views import * 
from campaigns.views import CampaignAdminApi,CampaigncategoryApi,ReportedCauseApi,SuccessfulCauseApi

urlpatterns = [
    
    # add general setting in the project 
    path('gs',GeneralSettingApi.as_view()),
    path('gs/<str:pk>',GeneralSettingApi.as_view()),
    
    # campaign catagories API
    path('category',CampaigncategoryApi.as_view()),
    path('category/<str:pk>',CampaigncategoryApi.as_view()),

    # add pages in the project 
    path('pages',PagesAPi.as_view()),
    path('pages/<str:pk>',PagesAPi.as_view()),

    # add Keywords API
    path('keyword',KeywordSApi.as_view()),
    path('keyword/<str:pk>',KeywordSApi.as_view()),

    # add limit data 
    path('limit',LimitApi.as_view()),
    path('limit/<str:pk>',LimitApi.as_view()),

    # add social Profile data
    path('social-media',SocialProfileApi.as_view()),
    path('social-media/<str:pk>',SocialProfileApi.as_view()),

    # Add landing Page API
    path('landing-page',LandingPageSettingApi.as_view()),
    path('landing-page/<str:pk>',LandingPageSettingApi.as_view()),

    # camapign Catagories api 
    path('campaign',CampaignAdminApi.as_view()),
    path('campaign/<str:pk>',CampaignAdminApi.as_view()),
    
    path('reported-campaign',ReportedCauseApi.as_view()),
    path('successful-campaign',SuccessfulCauseApi.as_view()),
    
    path('campaign-kyc',CampaignKycAPI.as_view()),
    path('campaign-kyc/<str:pk>',CampaignKycAPI.as_view()),
    
    path('dashboard-api',AdminDashboardApi.as_view()),
    path('donation-api',AdminDonationApi.as_view()),
    
    path('user-update/<str:pk>',UserUpdateApi.as_view()),
    
    path('donors',DonorsApi.as_view()),
    path('donors/<str:pk>',DonorsApi.as_view()),
    
    path('revision-history',RevisionHistoryAPi.as_view()),
    path('revision-history/<str:pk>',RevisionHistoryAPi.as_view())
    
    
]