from django.contrib import admin
from .models import * 
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin):
    readonly_fields = ('unique_id',)  # ✅ Mark as read-only to avoid FieldError

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'unique_id')}),
    )

admin.site.register(User, CustomUserAdmin)

class VehicleInline(admin.StackedInline):
    model = Vehicle
    extra = 1
    
class VehicleCategoryAdmin(admin.ModelAdmin):
    inlines = [VehicleInline]
    
admin.site.register(VehicleCategory, VehicleCategoryAdmin)

admin.site.register(Vehicle)

admin.site.register(Booking)

admin.site.register(EnquiryBooking)

admin.site.register(ProjectGallery)

admin.site.register(Services)

admin.site.register(HomePageSliderImage)

admin.site.register(AboutUsImages)