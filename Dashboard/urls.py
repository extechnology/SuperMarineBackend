from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

router = DefaultRouter()
router.register(r'vehicle-categories', VehicleCategoryViewSetDashboard)
router.register(r'vehicles', VehicleViewSetDashboard)
router.register(r'bookings', BookingViewSetDashboard)
router.register(r'enquiry-bookings', EnquiryBookingViewSetDashboard)
router.register(r'project-gallery', ProjectGalleryViewSetDashboard)
router.register(r'services', ServicesViewSetDashboard)
router.register(r'homepage-slider-images', HomePageSliderImageViewSetDashboard)
router.register(r'aboutus-images', AboutUsImagesViewSetDashboard)

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', DashboardTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
