from rest_framework import serializers
from .models import *


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse





class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')

        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))

        # Save OTP to the database
        EmailOTP.objects.update_or_create(email=validated_data['email'], defaults={'otp': otp})

        # Send OTP via email
        send_mail(
            'Your OTP Code',
            f'Your OTP for registration is: {otp}',
            'no-reply@yourdomain.com',
            [validated_data['email']],
            fail_silently=False,
        )

        return {'email': validated_data['email'], 'message': 'OTP sent to email'}


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            otp_instance = EmailOTP.objects.get(email=data['email'])
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError("Invalid email or OTP")

        if otp_instance.otp != data['otp']:
            raise serializers.ValidationError("Incorrect OTP")

        if not otp_instance.is_valid():
            raise serializers.ValidationError("OTP has expired")

        return data

    def create(self, validated_data):
        # Create user after OTP verification
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        # Remove OTP entry after successful registration
        EmailOTP.objects.filter(email=validated_data['email']).delete()

        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{self.context['request'].scheme}://{self.context['request'].get_host()}/api/employee/reset-password-confirm/{uid}/{token}/"
        
        subject = "Password Reset Requested"
        message = f"Hi your Username is : {user.username},\n\nClick the link below to reset your password:\n{reset_link}\n\nThis link will expire in 24 hours.\n\nIf you didn’t request this, ignore this email."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
        
        
class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
 





class VehicleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleCategory
        fields = '__all__'
        
class VehicleSerializer(serializers.ModelSerializer):
    category = VehicleCategorySerializer()
    class Meta:
        model = Vehicle
        fields = '__all__'
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        
class EnquiryBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnquiryBooking
        fields = '__all__'