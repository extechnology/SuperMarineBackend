from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view

# Models and serializers 

from .models import *
from .serializers import *

from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import stripe
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from django.utils.dateparse import parse_date,parse_time
from rest_framework import permissions
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
import os

# authentication


class GoogleAuthView(APIView):
    def post(self, request):
        token = request.data.get("token")  # frontend sends Google ID token

        if not token:
            return Response({"error": "ID token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the token with Google
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                os.getenv("GOOGLE_CLIENT_ID")  # must match your Google Cloud Console client ID
            )

            email = idinfo.get("email")
            username = idinfo.get("name") or email.split("@")[0]

            if not email:
                return Response({"error": "Invalid token: no email"}, status=status.HTTP_400_BAD_REQUEST)

            # Get or create user
            user, created = User.objects.get_or_create(email=email, defaults={"username": username})

            # Update username if newly created
            if created:
                user.username = username
                user.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response({"error": f"Invalid token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'OTP sent to email'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Account verified and created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(APIView):
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    
class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)

class EnquiryBookingView(APIView):
    def post(self, request):
        serializer = EnquiryBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VehicleView(APIView):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

class VehicleCategoryView(APIView):
    def get(self, request):
        categories = VehicleCategory.objects.all()
        serializer = VehicleCategorySerializer(categories, many=True)
        return Response(serializer.data)

class ProjectGalleryView(APIView):
    def get(self, request):
        gallery = ProjectGallery.objects.all()
        serializer = ProjectGallerySerializer(gallery, many=True)
        return Response(serializer.data)


class ServicesView(APIView):
    def get(self, request):
        services = Services.objects.all()
        serializer = ServicesSerializer(services, many=True)
        return Response(serializer.data)


class ServiceEnquiryView(APIView):
    def post(self, request):
        serializer = ServiceEnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Enquiry submitted successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class HomePageSliderImageView(APIView):
    def get(self, request):
        slider_images = HomePageSliderImage.objects.all()
        serializer = HomePageSliderImageSerializer(slider_images, many=True)
        return Response(serializer.data)

class AboutUsImagesView(APIView):
    def get(self, request):
        about_us_images = AboutUsImages.objects.all()
        serializer = AboutUsImagesSerializer(about_us_images, many=True)
        return Response(serializer.data)
    
class BookAdventureViewSet(viewsets.ModelViewSet):
    queryset = BookAdventure.objects.all()
    serializer_class = BookAdventureSerializer
    
class AboutUsContentViewSet(viewsets.ModelViewSet):
    queryset = AboutUsContent.objects.all()
    serializer_class = AboutUsContentSerializer
    
class ThrillMeetViewSet(viewsets.ModelViewSet):
    queryset = ThrillMeetsTrust.objects.all()
    serializer_class = ThrillMeetSerializer
    
class NumbersViewSet(viewsets.ModelViewSet):
    queryset = Numbers.objects.all()
    serializer_class = NumbersSerializer
    
class AdventureGalleryViewSet(viewsets.ModelViewSet):
    queryset = AdventureGallery.objects.all()
    serializer_class = AdventureGallerySerializer
    
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by("-created_at")
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
class GalleryBannerViewSet(viewsets.ModelViewSet):
    queryset = GalleryBanner.objects.all()
    serializer_class = GalleryBannerSerializer
    
class ContactBannerViewSet(viewsets.ModelViewSet):
    queryset = ContactBanner.objects.all()
    serializer_class = ContactBannerSerializer
    
class RentalBannerViewSet(viewsets.ModelViewSet):   
    queryset = RentalBanner.objects.all()
    serializer_class = RentalBannerSerializer
    
class ServiceBannerViewSet(viewsets.ModelViewSet):
    queryset = ServiceBanner.objects.all()
    serializer_class = ServiceBannerSerializer 
    

stripe.api_key = settings.STRIPE_SECRET_KEY

DURATION_MAP = {
    "30 mins": "00:30:00",
    "1 hour": "01:00:00",
    "2 hours": "02:00:00",
    "Full day": "08:00:00",
}

def parse_duration_to_td(s: str) -> timedelta:
    hh, mm, ss = [int(x) for x in s.split(":")]
    return timedelta(hours=hh, minutes=mm, seconds=ss)

def ensure_hhmmss(t: str) -> str:
    # "14:30" -> "14:30:00"
    return t if len(t) == 8 else f"{t}:00"

def calculate_total(base_price_30mins: Decimal, duration_label: str, people: int, discount_pct: Decimal) -> Decimal:
    multipliers = {
        "30 mins": Decimal("1"),   # Base
        "1 hour": Decimal("2"),
        "2 hours": Decimal("4"),
        "Full day": Decimal("16"), # 8 hours
    }
    base = base_price_30mins * multipliers.get(duration_label, Decimal("1"))
    subtotal = base * Decimal(people)
    discount = subtotal * (discount_pct / Decimal("100")) if discount_pct else Decimal("0")
    return (subtotal - discount).quantize(Decimal("0.01"))


@api_view(["POST"])
@permission_classes([permissions.AllowAny])  
def create_checkout_session(request):
    data = request.data
    print(request.data,"data------------------------------------")


    email = data.get("email")
    title = data.get("title", "Service")
    date_str = data.get("date")
    time_str = ensure_hhmmss(data.get("time", "10:00"))
    
    base_price = Decimal(str(data.get("base_price", "120.00"))) 
    duration_label = data.get("duration") or "30 mins"
    people = int(data.get("number_of_persons", 1))
    discount_pct = Decimal(str(data.get("discount", "0")))


    total = calculate_total(base_price, duration_label, people, discount_pct)

    amount_cents = int(total * 100)

    description = f"{title} — {duration_label}, {people} person(s) — {date_str} {time_str}"

    try:
      session = stripe.checkout.Session.create(
          mode="payment",
          payment_method_types=["card"],
          customer_email=email,  # optional
          line_items=[{
              "price_data": {
                  "currency": "aed", 
                  "product_data": {"name": title, "description": description},
                  "unit_amount": amount_cents,
              },
              "quantity": 1,
          }],
          success_url=f"{settings.FRONTEND_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
          cancel_url=f"{settings.FRONTEND_URL}/payment/cancel",
          metadata={
              # store everything you need to create the Booking after payment
              "title": title,
              "date": date_str or "",
              "time": time_str,
              "duration_label": duration_label,
              "number_of_persons": str(people),
              "email": email or "",
              "discount": str(discount_pct),
              "price_per_hour": str(base_price),
          },
      )
      return Response({"checkout_url": session.url, "id": session.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        import traceback
        traceback.print_exc()  # Logs the full stack trace
        print("Stripe error:", e)  # This now works because e is in scope
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        meta = session.get("metadata", {})

        # Build/save the Booking here (payment succeeded)
        title = meta.get("title", "Service")
        date = parse_date(meta.get("date") or "")
        time = parse_time(meta.get("time") or "10:00:00")
        duration_label = meta.get("duration_label", "1 hour")
        num_people = int(meta.get("number_of_persons", "1"))
        email = meta.get("email", "")
        discount_pct = Decimal(meta.get("discount", "0"))
        price_per_hour = Decimal(meta.get("price_per_hour", "0"))

        # Pick a duration for the model's DurationField
        dur = DURATION_MAP.get(duration_label, "01:00:00")
        duration_td = parse_duration_to_td(dur)

        amount_total = Decimal(session.get("amount_total", 0)) / Decimal("100")

        Booking.objects.create(
            title=title,
            price=amount_total,
            duration=duration_td,
            time=time,
            date=date,
            name=meta.get("name", ""),  
            email=email,
            phone=meta.get("phone", ""),
            special_request=meta.get("notes", None),
            discount=discount_pct,
            number_of_persons=num_people,
        )

    return HttpResponse(status=200)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_session(request, session_id: str):
    session = stripe.checkout.Session.retrieve(session_id)
    return Response({
        "status": session.get("status"),
        "payment_status": session.get("payment_status"),
        "amount_total": (Decimal(session.get("amount_total", 0)) / Decimal("100")),
        "currency": session.get("currency"),
        "metadata": session.get("metadata", {}),
    })
    