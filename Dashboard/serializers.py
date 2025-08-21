from rest_framework import serializers
from Application.models import *



from .custom_permissions import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        if not user.is_staff and not user.is_superuser:
            raise serializers.ValidationError("You are not authorized to access the dashboard.")

        # Optionally add custom user info
        data['username'] = user.username
        data['email'] = user.email
        data['is_staff'] = user.is_staff
        data['is_superuser'] = user.is_superuser

        return data

class VehicleCategorySerializerDashboard(serializers.ModelSerializer):
    class Meta:
        model = VehicleCategory
        fields = '__all__'
        
class VehicleDurationSerializerDashboard(serializers.ModelSerializer):
    class Meta:
        model = VehicleDuration
        fields = '__all__'
        
class VehicleSerializerDashboard(serializers.ModelSerializer):
    category = VehicleCategorySerializerDashboard()
    duration = VehicleDurationSerializerDashboard(many=True)
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
        
        
class ServiceEnquirySerializerDashboard(serializers.ModelSerializer):
    class Meta:
        model = ServiceEnquiry
        fields = '__all__'