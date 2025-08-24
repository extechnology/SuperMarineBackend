from rest_framework import serializers
from .models import *


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings


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
        
        # Create HTML email template with dark theme
        html_message = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Your OTP Code</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    background-color: #0f0f23;
                    color: #e4e4e7;
                    line-height: 1.6;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 40px 20px;
                }}
                .card {{
                    background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3a 100%);
                    border-radius: 16px;
                    padding: 40px;
                    border: 1px solid #3f3f46;
                    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                
                .title {{
                    font-size: 28px;
                    font-weight: 700;
                    color: #f8fafc;
                    margin: 0 0 10px 0;
                }}
                .subtitle {{
                    font-size: 16px;
                    color: #94a3b8;
                    margin: 0;
                }}
                .content {{
                    margin: 30px 0;
                }}
                .message {{
                    font-size: 16px;
                    color: #cbd5e1;
                    margin-bottom: 30px;
                    text-align: center;
                }}
                .otp-container {{
                    text-align: center;
                    margin: 30px 0;
                }}
                .otp-code {{
                    display: inline-block;
                    background: linear-gradient(135deg, #1e40af, #7c3aed);
                    color: white;
                    font-size: 32px;
                    font-weight: 800;
                    letter-spacing: 8px;
                    padding: 20px 40px;
                    border-radius: 12px;
                    border: 2px solid #3b82f6;
                    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
                    font-family: 'Courier New', monospace;
                }}
                .warning {{
                    background: rgba(239, 68, 68, 0.1);
                    border: 1px solid rgba(239, 68, 68, 0.3);
                    border-radius: 8px;
                    padding: 16px;
                    margin: 20px 0;
                    font-size: 14px;
                    color: #fca5a5;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #374151;
                }}
                .footer-text {{
                    font-size: 12px;
                    color: #6b7280;
                    margin: 5px 0;
                }}
                .divider {{
                    height: 1px;
                    background: linear-gradient(90deg, transparent, #374151, transparent);
                    margin: 30px 0;
                }}
                .highlight {{
                    color: #60a5fa;
                    font-weight: 600;
                }}
                @media (max-width: 480px) {{
                    .container {{ padding: 20px 10px; }}
                    .card {{ padding: 25px 20px; }}
                    .otp-code {{ 
                        font-size: 28px; 
                        letter-spacing: 6px; 
                        padding: 15px 25px; 
                    }}
                    .title {{ font-size: 24px; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="card">
                    <div class="header">
                        <h1 class="title">Verification Code</h1>
                        <p class="subtitle">Complete your registration</p>
                    </div>
                    
                    <div class="content">
                        <p class="message">
                            Hi there! 👋<br>
                            We've sent you this <span class="highlight">6-digit verification code</span> to complete your registration.
                        </p>
                        
                        <div class="otp-container">
                            <div class="otp-code">{otp}</div>
                        </div>
                        
                        <div class="warning">
                            ⚠️ <strong>Security Notice:</strong> This code will expire in 5 minutes. Never share this code with anyone for your security.
                        </div>
                        
                        <div class="divider"></div>
                        
                        <p style="text-align: center; color: #94a3b8; font-size: 14px;">
                            If you didn't request this code, please ignore this email or contact our support team.
                        </p>
                    </div>
                    
                    <div class="footer">
                        <p class="footer-text">This email was sent automatically. Please do not reply.</p>
                        <p class="footer-text">© 2024 supermarinerental.com. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Send OTP via email with HTML content
        send_mail(
            'Your OTP Code - Verification Required',
            f'Your OTP for registration is: {otp}',  # Plain text fallback
            'no-reply@yourdomain.com',
            [validated_data['email']],
            fail_silently=False,
            html_message=html_message,  # HTML version
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

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get("email")

        try:
            otp_record = EmailOTP.objects.get(email=email)
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "No OTP found. Please request a new one."}
            )

        # Check if OTP is still valid
        expiration_time = otp_record.created_at + timedelta(minutes=5)
        if now() <= expiration_time:
            otp = otp_record.otp  # Use the existing OTP
        else:
            # Generate a new OTP
            otp = str(random.randint(100000, 999999))
            otp_record.otp = otp
            otp_record.created_at = now()
            otp_record.save()
            
        data["otp"] = otp  

        # ✅ Add OTP to validated data if you need it later
        # data["otp"] = otp
        # return data

        html_message = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resend OTP Code</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    background-color: #0f0f23;
                    color: #e4e4e7;
                    line-height: 1.6;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 40px 20px;
                }}
                .card {{
                    background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3a 100%);
                    border-radius: 16px;
                    padding: 40px;
                    border: 1px solid #3f3f46;
                    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .title {{
                    font-size: 28px;
                    font-weight: 700;
                    color: #f8fafc;
                    margin: 0 0 10px 0;
                }}
                .subtitle {{
                    font-size: 16px;
                    color: #94a3b8;
                    margin: 0;
                }}
                .content {{
                    margin: 30px 0;
                }}
                .message {{
                    font-size: 16px;
                    color: #cbd5e1;
                    margin-bottom: 30px;
                    text-align: center;
                }}
                .resend-notice {{
                    background: rgba(245, 158, 11, 0.1);
                    border: 1px solid rgba(245, 158, 11, 0.3);
                    border-radius: 8px;
                    padding: 16px;
                    margin: 20px 0;
                    text-align: center;
                    font-size: 14px;
                    color: #fbbf24;
                }}
                .otp-container {{
                    text-align: center;
                    margin: 30px 0;
                }}
                .otp-code {{
                    display: inline-block;
                    background: linear-gradient(135deg, #dc2626, #ea580c);
                    color: white;
                    font-size: 32px;
                    font-weight: 800;
                    letter-spacing: 8px;
                    padding: 20px 40px;
                    border-radius: 12px;
                    border: 2px solid #ef4444;
                    box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
                    font-family: 'Courier New', monospace;
                }}
                .warning {{
                    background: rgba(239, 68, 68, 0.1);
                    border: 1px solid rgba(239, 68, 68, 0.3);
                    border-radius: 8px;
                    padding: 16px;
                    margin: 20px 0;
                    font-size: 14px;
                    color: #fca5a5;
                }}
                .info-box {{
                    background: rgba(59, 130, 246, 0.1);
                    border: 1px solid rgba(59, 130, 246, 0.3);
                    border-radius: 8px;
                    padding: 16px;
                    margin: 20px 0;
                    font-size: 14px;
                    color: #93c5fd;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #374151;
                }}
                .footer-text {{
                    font-size: 12px;
                    color: #6b7280;
                    margin: 5px 0;
                }}
                .divider {{
                    height: 1px;
                    background: linear-gradient(90deg, transparent, #374151, transparent);
                    margin: 30px 0;
                }}
                .highlight {{
                    color: #fbbf24;
                    font-weight: 600;
                }}
                .time-notice {{
                    display: inline-flex;
                    align-items: center;
                    background: rgba(16, 185, 129, 0.1);
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 20px;
                    padding: 8px 16px;
                    margin: 10px 0;
                    font-size: 12px;
                    color: #6ee7b7;
                }}
                @media (max-width: 480px) {{
                    .container {{ padding: 20px 10px; }}
                    .card {{ padding: 25px 20px; }}
                    .otp-code {{ 
                        font-size: 28px; 
                        letter-spacing: 6px; 
                        padding: 15px 25px; 
                    }}
                    .title {{ font-size: 24px; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="card">
                    <div class="header">
                        <h1 class="title">New Verification Code</h1>
                        <p class="subtitle">Your fresh OTP is ready</p>
                    </div>
                    <div class="content">
                        <div class="resend-notice">
                            🔄 <strong>Code Resent!</strong> We've generated a new verification code for you.
                        </div>
                        <p class="message">
                            Here's your <span class="highlight">new 6-digit verification code</span>.<br>
                            Your previous code has been invalidated for security.
                        </p>
                        <div class="otp-container">
                            <div class="otp-code">{otp}</div>
                        </div>
                        <div class="info-box">
                            💡 <strong>Why did you receive this?</strong><br>
                            Someone (hopefully you!) requested a new verification code. This could be because:
                            <ul style="margin: 8px 0; padding-left: 20px; color: #93c5fd;">
                                <li>Your previous code expired</li>
                                <li>You didn't receive the first email</li>
                                <li>You requested a fresh code</li>
                            </ul>
                        </div>
                        <div class="warning">
                            ⚠️ <strong>Security Notice:</strong> This new code will expire in 5 minutes. Your previous verification code is no longer valid.
                        </div>
                        <div class="divider"></div>
                        <p style="text-align: center; color: #94a3b8; font-size: 14px;">
                            If you didn't request this resend, please secure your account immediately or contact our support team.
                        </p>
                    </div>
                    <div class="footer">
                        <p class="footer-text">This email was sent automatically. Please do not reply.</p>
                        <p class="footer-text">© 2025 supermarinerental.com. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        # Send OTP via email with HTML content
        send_mail(
            'New OTP Code - Verification Resent',
            f'Your new OTP for verification is: {otp}',  # Plain text fallback
            'no-reply@yourdomain.com',
            [email],
            fail_silently=False,
            html_message=html_message,  # HTML version
        )
        return data 
            
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        request = self.context.get("request")
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        frontend_url = f"http://localhost:5173/reset-password/{uid}/{token}"

        subject = "Password Reset Requested"
        text_message = f"Hi {user.username},\n\nClick the link below:\n{frontend_url}"
        html_message = f"""
        <p>Hi <b>{user.username}</b>,</p>
        <p>Click the link below to reset your password:</p>
        <p><a href="{frontend_url}">{frontend_url}</a></p>
        <p>This link will expire in 24 hours.</p>
        """

        email_msg = EmailMultiAlternatives(subject, text_message, settings.EMAIL_HOST_USER, [email])
        email_msg.attach_alternative(html_message, "text/html")
        email_msg.send()


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid reset link.")

        if not default_token_generator.check_token(self.user, data['token']):
            raise serializers.ValidationError("Invalid or expired token.")

        return data

    def save(self):
        password = self.validated_data['password']
        self.user.set_password(password)
        self.user.save()
        return self.user


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
        
class ProjectGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectGallery
        fields = '__all__'
        
class ServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Services
        fields = '__all__'


class ServiceEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceEnquiry
        fields = '__all__'
        

class HomePageSliderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageSliderImage
        fields = '__all__'

class AboutUsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsImages
        fields = '__all__'
        
class ThrillMeetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThrillMeetsTrust
        fields = '__all__'
        
        
class NumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Numbers
        fields = '__all__'
        
class AdventureGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdventureGallery
        fields = '__all__'
        
        
class BookAdventureSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAdventure
        fields = '__all__'
        

class AboutUsContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsContent
        fields = '__all__'
        
        
        
class GalleryBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryBanner
        fields = '__all__'
        
class ContactBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactBanner
        fields = '__all__'
        
        
class ServiceBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBanner
        fields = '__all__'
        
        
class RentalBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalBanner
        fields = '__all__'
        
        
