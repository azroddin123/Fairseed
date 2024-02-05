from django.urls import path
from .views import * 
# from campaigns.views import CampaignAdminApi
urlpatterns = [
    # add general setting in the project 
    path('gs',GeneralSettingApi.as_view()),
    path('gs/<str:pk>',GeneralSettingApi.as_view()),

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


    # path('campaign-admin',CampaignAdminApi.as_view()),
    # path('campaign-admin/<str:pk>',CampaignAdminApi.as_view()),

####################################################################
    path('pages-admin',PagesAPI.as_view()),
    path('pages-admin/<str:pk>',PagesAPI.as_view()),
    path('PageCreate/',PageCreate.as_view()),

    



]