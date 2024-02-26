from django.urls import path
from .views import * 


urlpatterns = [
    path('user',UserApi.as_view()),
    path('user/<str:pk>', UserApi.as_view()),
    
    path('user-roles',UserRolesAPi.as_view()),
    path('user-roles/<str:pk>', UserRolesAPi.as_view()),
    
    path('register/nt/',RegisterUserApi.as_view()),
    path('user/nt/',UserApi.as_view()),
    path('change_password',ChangePasswordApi.as_view()),
    path('login/nt/',LoginAPI.as_view()),
    path('forgetpassword',ForgotPasswordAPI.as_view()),
    path('reset-pass',ResetPasswordAPI.as_view())
]
