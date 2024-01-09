from django.urls import path
from .views import * 


urlpatterns = [
    path('user',UserApi.as_view()),
    path('user/<str:pk>', UserApi.as_view()),
    path('register/nt/',RegisterUserApi.as_view()),
    path('user/nt/',UserApi.as_view()),
    path('change_password',ChangePasswordApi.as_view()),
    # path('test/<int:id1>/<int:id2>/<int:id3>/', PassIdApi.as_view()),

    ###################################################
    path('send-email/', EmailSMTP.as_view(), name='send-email'),
    path('register-new',RegisterApi.as_view()),
    path('register-update/<str:pk>/', RegisterApi.as_view()),
    ###################################################
    
]
