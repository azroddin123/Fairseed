from django.urls import path
from .views import * 

urlpatterns = [
    # add general setting in the project 
    path('gs',GeneralSettingApi.as_view()),
    path('gs/<int:pk>',GeneralSettingApi.as_view()),

    # add pages in the project 
    path('pages',PagesAPi.as_view()),
    path('pages/<int:pk>',PagesAPi.as_view()),

    # add Keywords API
    path('keyword',KeywordSApi.as_view()),
    path('keyword/<int:pk>',KeywordSApi.as_view()),

    # add limit data 
    path('limit',LimitApi.as_view()),
    path('limit/<int:pk>',LimitApi.as_view()),

    # add social Profile data

    path('social-media',SocialProfileApi.as_view()),
    path('social-media/<int:pk>',SocialProfileApi.as_view()),

    # Add landing Page API
    path('landing-page',LandingPageApi.as_view()),
    path('landing-page/<int:pk>',LandingPageApi.as_view())

]