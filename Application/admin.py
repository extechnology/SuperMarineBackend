from django.contrib import admin
from .models import * 
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin): 
    readonly_fields = ('unique_id',)  

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

admin.site.register(VehicleDuration)

admin.site.register(Booking)

admin.site.register(EnquiryBooking)

admin.site.register(ProjectGallery)

admin.site.register(HomePageSliderImage)

admin.site.register(AboutUsImages)

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ("title", "click_count", "last_clicked")

    def click_count(self, obj):
        return obj.clicks.count()

    def last_clicked(self, obj):
        last = obj.clicks.order_by("-created_at").first()
        return last.created_at if last else "-"

