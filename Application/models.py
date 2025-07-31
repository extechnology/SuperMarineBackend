from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

from django.utils.timezone import now
import random
from django.core.mail import send_mail
from datetime import timedelta
import pytz

class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """Store created_at in IST (Asia/Kolkata) timezone"""
        ist = pytz.timezone('Asia/Kolkata')
        self.created_at = now().astimezone(ist)
        super().save(*args, **kwargs)

    def is_valid(self):
        """OTP expires in 5 minutes"""
        ist = pytz.timezone('Asia/Kolkata')
        expiration_time = self.created_at + timedelta(minutes=5)
        return now().astimezone(ist) <= expiration_time

    def __str__(self):
        return f'{self.email} - {self.otp} - {self.created_at.astimezone(pytz.timezone("Asia/Kolkata"))}'
    

class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    

class VehicleCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.name)
    
    
class Vehicle(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(VehicleCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='vehicle_images/', null=True, blank=True)
    capacity = models.PositiveIntegerField()
    duration = models.DurationField()
    discount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name - self.category.name)


class Booking(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()
    time = models.TimeField()
    date = models.DateField()
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    special_request = models.TextField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    number_of_persons = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.name} on {self.date}"
    

class EnquiryBooking(models.Model):
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    time = models.TimeField()
    date = models.DateField()
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    number_of_persons = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} - {self.name} on {self.date}"
    
class ProjectGallery(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gallery_images/')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Services(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='services_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class HomePageSliderImage(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    image = models.ImageField(upload_to='slider_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AboutUsImages(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='about_us_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
