from django.urls import path
from .views import * 


urlpatterns = [
    path('user',UserApi.as_view()),
    path('user/<int:pk>', UserApi.as_view()),
    path('register/nt/',RegisterUserApi.as_view()),
    path('user/nt/',UserApi.as_view()),
    path('change_password',ChangePasswordApi.as_view()),
    path('test/<int:id1>/<int:id2>/<int:id3>/', PassIdApi.as_view()),
    # email verification apiview

    ##################################################

    path('register1/',RegisterAPI.as_view()),
    path('register1/<int:pk>/',RegisterAPI.as_view()),
    
]
