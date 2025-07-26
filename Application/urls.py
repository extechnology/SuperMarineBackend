from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

urlpatterns = [
    
    
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend-otp'),
    path('google-auth/', views.GoogleAuthView.as_view(), name='google-auth'),
    path('password-reset-request/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('enquiry-booking/', views.EnquiryBookingView.as_view(), name='booking'),
    
    path('vehicle/', views.VehicleView.as_view(), name='vehicle'),
    path('vehicle-category/', views.VehicleCategoryView.as_view(), name='vehicle-category'),
]
