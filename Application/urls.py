from django.urls import path,include
from . import views
from .views import CustomTokenObtainPairView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'bookings', views.BookingViewSet, basename='bookings')
router.register(r'adventure/gallery', views.AdventureGalleryViewSet, basename='adventure-gallery')
router.register(r'numbers', views.NumbersViewSet, basename='numbers')
router.register(r'thrill/meet', views.ThrillMeetViewSet, basename='thrill-meet')
router.register(r'book/adventure', views.BookAdventureViewSet, basename='book-adventure')
router.register(r'about/content', views.AboutUsContentViewSet, basename='about-content')
router.register(r'gallery/banner', views.GalleryBannerViewSet, basename='gallery-banner')
router.register(r'contact/banner', views.ContactBannerViewSet, basename='contact-banner')
router.register(r'rental/banner', views.RentalBannerViewSet, basename='rental-banner')
router.register(r'service/banner', views.ServiceBannerViewSet, basename='service-banner')

urlpatterns = [
    
    path('api/', include(router.urls)),
    
    path('google-auth/', views.GoogleAuthView.as_view(), name='google-auth'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend-otp'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("password-reset/", views.PasswordResetView.as_view(), name="password-reset"),
    path("password-reset-confirm/", views.PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    
    path('enquiry-booking/', views.EnquiryBookingView.as_view(), name='booking'),
    
    path('vehicle/', views.VehicleView.as_view(), name='vehicle'),
    
    path('vehicle-category/', views.VehicleCategoryView.as_view(), name='vehicle-category'),
    
    path('project-gallery/', views.ProjectGalleryView.as_view(), name='project-gallery'),
    
    path('services/',views.ServicesView.as_view(), name='service'),
    
    path('service/enquiry/', views.ServiceEnquiryView.as_view(), name='service-enquiry'),
    
    path('home-page-slider/',views.HomePageSliderImageView.as_view(), name='slider-image'),
    
    path('about-us-slider/',views.AboutUsImagesView.as_view(), name='about-us-slider'),
    
    path("api/payments/create-checkout-session/", views.create_checkout_session, name="create-checkout-session"),
    
    path("api/payments/webhook/", views.stripe_webhook, name="stripe-webhook"),
    
    path("api/payments/session/<str:session_id>/", views.get_session, name="stripe-session"),
]
