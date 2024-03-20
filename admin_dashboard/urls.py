from django.urls import path
from .views import * 
from accounts.views import * 
from campaigns.views import CampaigncategoryApi,ReportedCauseApi,SuccessfulCauseApi
from payment_gateways.views import PhonepayApi
urlpatterns = [
    
    # add general setting in the project 
    path('gs',GeneralSettingApi.as_view()),
    path('gs/<str:pk>',GeneralSettingApi.as_view()),
    
    # campaign catagories API
    path('category',CampaigncategoryApi2.as_view()),
    path('category/<str:pk>',CampaigncategoryApi2.as_view()),

    # add pages in the project 
    path('pages',PagesAPi.as_view()),
    path('pages/<str:pk>',PagesAPi.as_view()),

    # path('slug/<str:slug>',PagesSlugApi.as_view()),

    # add Keywords API
    path('keyword',KeywordSApi.as_view()),
    path('keyword/<str:pk>',KeywordSApi.as_view()),

    # add limit data str:pk>
    path('limit',LimitApi.as_view()),
    path('limit/<str:pk>',LimitApi.as_view()),

    # add social Profile data
    path('social-media',SocialProfileApi.as_view()),
    path('social-media/<',SocialProfileApi.as_view()),

    # Add landing Page API
    path('cause-edit',CampaignEditApproval.as_view()),
    path('cause-edit/<str:pk>',CampaignEditApproval.as_view()),
    

    path('landing-page',LandingPageSettingApi.as_view()),
    path('landing-page/<str:pk>',LandingPageSettingApi.as_view()),

    # camapign Catagories api 
    path('campaign',CampaignAdminApi2.as_view()),
    path('campaign/<str:pk>',CampaignAdminApi2.as_view()),
    
    path('reported-campaign',ReportedCauseApi.as_view()),
    path('successful-campaign',SuccessfulCauseApi.as_view()),
    
    path('campaign-kyc',CampaignKycAPI.as_view()),
    path('campaign-kyc/<str:pk>',CampaignKycAPI.as_view()),
    
    path('dashboard-api',AdminDashboardApi.as_view()),
    path('donation-api',AdminDonationApi.as_view()),
    
    path('countrywise-users',AdminCountryApi.as_view()),
    
    path('user-update/<str:pk>',UserUpdateApi.as_view()),
    
    path('donors',DonorsApi.as_view()),
    path('donors/<str:pk>',DonorsApi.as_view()),
    
    path('documents',DocumentAPI.as_view()),
    path('documents/<str:pk>',DocumentAPI.as_view()),
  
    path('revise-history/<str:pk>',RevisionHistoryApi.as_view()),
    
    path('users',UserApi2.as_view()),
    path('users/<str:pk>',UserApi2.as_view()),
    
    path('user-roles',UserRolesAPi.as_view()),
    path('user-roles/<str:pk>',UserRolesAPi.as_view()),
    
    path('phonepay',PhonepayApi.as_view()),
    path('phonepay/<str:pk>',UserApi.as_view()),

    path('withdrawals',WithdrawalApi.as_view()),
    path('withdrawals/<str:pk>',WithdrawalApi.as_view()),

    path('donation-graph',DonationGraphAPI.as_view()),

    path('cause-edit1',CausEditApi.as_view()),
    path('cause-edit1/<str:pk>',CausEditApi.as_view()),
]