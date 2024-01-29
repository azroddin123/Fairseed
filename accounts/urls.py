from django.urls import path
from .views import * 


urlpatterns = [
    path('user',UserApi.as_view()),
    path('user/<str:pk>', UserApi.as_view()),
    path('register/nt/',RegisterUserApi.as_view()),
    path('user/nt/',UserApi.as_view()),
    path('api/change_password/',ChangePasswordApi.as_view()),
    # path('test/<int:id1>/<int:id2>/<int:id3>/', PassIdApi.as_view()),

    ###########################################################################
    
    #Admin Panel Dashboard latest members(rest 2 api's in campaign urls.py)
    path('api/admin/latest-members/',LatestMembers.as_view()),
    
    path('api/send-email/', RegisterOTPApi.as_view()),
    path('api/verify-otp/',VerifyOTPApi.as_view()),
    path('api/login/',LoginView.as_view()),
    path('api/send-message/',EmailSMTP.as_view()),
    path('api/register-new/',RegisterApi.as_view()),
    path('api/register-new/<str:pk>/', RegisterApi.as_view()),
    path('api/forgot-password/', ForgotPasswordApi.as_view()),
    path('api/verification-password/', VerificationOtpApi.as_view()),
    path('api/set-new-password/', SetNewPasswordApi.as_view()),
    path('api/admin/user/',User_AdminPanel.as_view()), #Admin Panel
    path('api/admin/user/<str:pk>/',User_AdminPanel.as_view()), #Admin Panel
    path('api/change-password/', UserChangePasswordSettingView.as_view(), name='change-password'),
    path('api/change-password/<str:pk>/', UserChangePasswordSettingView.as_view(), name='change-password'),
    path('api/admin/user_card/',UserEditCard_AdminPanel.as_view()),
    ###########################################################################
    
]
