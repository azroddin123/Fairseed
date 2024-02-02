from django.urls import path
from .views import * 


urlpatterns = [
    path('user',UserApi.as_view()),
    path('user/<str:pk>', UserApi.as_view()),
    path('register/nt/',RegisterUserApi.as_view()),
    path('user/nt/',UserApi.as_view()),
    path('change_password/',ChangePasswordApi.as_view()),
    path('test/<int:id1>/<int:id2>/<int:id3>/', PassIdApi.as_view()),
    # email verification apiview

    ##################################################

    path('api/register/userlist/',RegisterUserListAPI.as_view()),
    path('api/register/user/<int:id>/',RegisterUserAPI.as_view()),
    path('api/register/createuser/',RegisterPostAPI.as_view()),
    path('api/register/user/<int:pk>',RegisterApi.as_view()),
    
    
    # path('test/<int:id1>/<int:id2>/<int:id3>/', PassIdApi.as_view()),

    ###################################################
    path('register-new/',RegisterUserApi.as_view()),
    path('register-otp/',RegisterOTPApi.as_view()),
    path('verify-otp/',VerifyOTPApi.as_view()),
    path('changepass-otp/',ChangePassOTPApi.as_view()),
    path('loginapi/',LoginView.as_view()),
    path('logoutapi/', LogoutView.as_view(), name='logout'),
    
    path('api/admin/user/',User_AdminPanel.as_view()), #Admin Panel
    path('api/admin/user/<str:pk>/',User_AdminPanel.as_view()), #Admin Panel




]
