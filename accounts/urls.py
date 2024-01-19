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
    path('api/send-email/', RegisterOTPApi.as_view()),
    path('api/verify-otp/',VerifyOTPApi.as_view()),
    path('api/login/',LoginView.as_view()),
    path('api/send-message/',EmailSMTP.as_view()),
    path('api/register-new/',RegisterApi.as_view()),
    path('api/register-new/<str:pk>/', RegisterApi.as_view()),
    path('api/forgot-password/', ForgotPasswordApi.as_view()),
    path('api/verification-password/', VerificationOtpApi.as_view()),
    path('api/set-new-password/', SetNewPasswordApi.as_view()),
    path('api/admin/latest-members/',LatestMembers.as_view()),
    ###########################################################################
    
]
