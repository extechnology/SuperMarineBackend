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
router.register(r'service/enquiry', ServiceEnquiryViewSetDashboard)

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', DashboardTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("export/bookings/", ExportBookingsExcel.as_view(), name="export-bookings"),
    path("export/service-requests/", ExportServiceRequestsExcel.as_view(), name="export-service-requests"),
    path("export/enquiry-bookings/", ExportEnquiryBookingExcel.as_view(), name="export-enquiry-bookings"),
    path("bookings/<int:pk>/status/", UpdateBookingStatusView.as_view(), name="update-booking-status"),
    path("enquiry/<int:pk>/status/", UpdateEnquiryStatusView.as_view(), name="update-enquiry-status"),
    path("service/<int:pk>/status/", UpdateServiceStatusView.as_view(), name="update-service-status"),



]
