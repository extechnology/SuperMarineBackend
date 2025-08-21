from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets

from .serializers import *
from Application.models import *


class DashboardTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class DashboardTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class VehicleCategoryViewSetDashboard(viewsets.ModelViewSet):
    queryset = VehicleCategory.objects.all()
    serializer_class = VehicleCategorySerializerDashboard
    permission_classes = [IsSuperuserOrStaff]

class VehicleViewSetDashboard(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializerDashboard
    permission_classes = [IsSuperuserOrStaff]

class BookingViewSetDashboard(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializerDashboard
    permission_classes = [IsSuperuserOrStaff]

class EnquiryBookingViewSetDashboard(viewsets.ModelViewSet):
    queryset = EnquiryBooking.objects.all()
    serializer_class = EnquiryBookingSerializerDashboard
    permission_classes = [IsSuperuserOrStaff]

class ProjectGalleryViewSetDashboard(viewsets.ModelViewSet):
    queryset = ProjectGallery.objects.all()
    serializer_class = ProjectGallerySerializerDashboard
    permission_classes = [IsSuperuserOrStaff]

class ServicesViewSetDashboard(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializerDashboard
    permission_classes = [IsSuperuserOrStaff]

class HomePageSliderImageViewSetDashboard(viewsets.ModelViewSet):
    queryset = HomePageSliderImage.objects.all()
    serializer_class = HomePageSliderImageSerializerDashboard
    permission_classes = [IsSuperuserOrStaff]

class AboutUsImagesViewSetDashboard(viewsets.ModelViewSet):
    queryset = AboutUsImages.objects.all()
    serializer_class = AboutUsImagesSerializerDashboard
    permission_classes = [IsSuperuserOrStaff]
    
    
class ServiceEnquiryViewSetDashboard(viewsets.ModelViewSet):
    queryset = ServiceEnquiry.objects.all()
    serializer_class = ServiceEnquirySerializerDashboard
    permission_classes = [IsSuperuserOrStaff]