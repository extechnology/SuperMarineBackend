from rest_framework import serializers
from Application.models import *


class VehicleCategorySerializerDashboard(serializers.ModelSerializer):
    class Meta:
        model = VehicleCategory
        fields = '__all__'
        
class VehicleSerializerDashboard(serializers.ModelSerializer):
    category = VehicleCategorySerializerDashboard()
    class Meta:
        model = Vehicle
        fields = '__all__'
        
class BookingSerializerDashboard(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        
class EnquiryBookingSerializerDashboard(serializers.ModelSerializer):
    class Meta:
        model = EnquiryBooking
        fields = '__all__'
        
class ProjectGallerySerializerDashboard(serializers.ModelSerializer):
    class Meta:
        model = ProjectGallery
        fields = '__all__'
        
class ServicesSerializerDashboard(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class HomePageSliderImageSerializerDashboard(serializers.ModelSerializer):
    class Meta:
        model = HomePageSliderImage
        fields = '__all__'

class AboutUsImagesSerializerDashboard(serializers.ModelSerializer):
    class Meta:
        model = AboutUsImages
        fields = '__all__'