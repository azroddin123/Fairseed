from django.urls import path

from .views import *

urlpatterns = [   
    path('campaign-category',CampaigncategoryApi.as_view()),
    path('campaign-category/<str:pk>',CampaigncategoryApi.as_view()),

    path('campaign-details',CKBApi.as_view()),
    path('campaign-details/<str:pk>',CKBApi.as_view()),

    # path('kyc-details',KycApi.as_view()),
    # path('kyc-details/<str:pk>',KycApi.as_view()),

    path('documents',DocumentApi.as_view()),
    path('documents/<str:pk>',DocumentApi.as_view()),


    path('landing-page',LandingPageApi.as_view()),
    path('campaign-filter',CampaignFilterApi.as_view()),
    path('campaign/<str:pk>', CampaignDetailsApi.as_view()),
    path('campaign', CampaignDetailsApi.as_view()),
    path('catagory', CampaignByCategoryApi.as_view()),

    # path('campaign/<str:pk>/', CampaignDetailsApi.as_view(), name='campaign-details'),
    # path('campaign/', CampaignDetailsApi.as_view(), name='campaign-list'),
    # path('category/', CampaignByCategoryApi.as_view(), name='campaign-by-category'),
    #################################################################################################################################
    # path('card/', CardAPIView.as_view()),
    path('api/campaign_category/',CampaignCategory1.as_view()),
    path('api/campaign_category/<str:pk>/',CampaignCategory1.as_view()),
    path('api/campaign_list/',CampaignDetailsApi1.as_view()),
    path('api/admin/dashboard/', DashboardAPI.as_view(), name='dashboard-api'),
    path('api/landing_page/causes_by_category/',CausesbyCategoryAPI.as_view()),
    path('api/landing_page/card/', CardAPIViewPagination.as_view()),
    path('api/cardview2/<str:pk>/',CardAPIView2.as_view()),
    path('api/recent_donors',RecentDonors.as_view()),
    # path('api/recent_donor/<str:pk>',RecentDonors.as_view()),
    path('api/admin/recent_campaigns/',RecentCampaigns.as_view()),
    path('api/admin/categories/<str:pk>/',CategoryAdminApi.as_view()),
    path('api/admin/categories/',CategoryAdminApi.as_view()),
    path('api/admin/campaign/', CampaignAdminApi.as_view()),
    path('api/admin/campaign/<str:pk>/', CampaignAdminApi.as_view()),
    path('api/admin/campaign_edit_Approval/',CampaignEditApproval.as_view()),
    path('api/admin/campaign_edit_Approval/<str:pk>/',CampaignEditApproval.as_view()),
    path('api/admin/scholarship_campaigns/',ScholarshipCAmpaigns.as_view()),
    path('api/admin/scholarship_campaigns/<str:pk>/',ScholarshipCAmpaigns.as_view()),
    path('api/admin/reported_campaigns/',ReportedCampaigns.as_view()),
    path('api/admin/reported_campaigns/<uuid:pk>/',ReportedCampaigns.as_view()),
    path('api/donate_page_card/<str:pk>/',DonateToCampaignCard.as_view()), #Donate To Campaign Page Card
    path('api/successful_campaigns/',CampaignBycategory.as_view()), #Successful campaign page
    path('api/admin/withdrawal/',WithdrawalCampaignView.as_view()), #Admin panel existing Withdrawal
    # path('api/admin/withdrawal_inside/<str:pk>',WithdrawalInsideView.as_view()), #Admin panel existing Withdrawal
    # path('api/admin/ckb/',CampaignKycBenificiaryAPI.as_view()), # Admin Panel
    # path('api/admin/ckb/<str:pk>/',CampaignKycBenificiaryAPI.as_view()), # Admin Panel
    ##############################################################################################################################


]