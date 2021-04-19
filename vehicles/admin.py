from django.contrib import admin
from .models import Vehicle, VehicleBrand, VehicleImages, Messages


class MessagesAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message', 'timestamp', 'is_read']


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'description', 'price',
                    'seat_capacity', 'availability', 'current_location']


admin.site.register(Messages, MessagesAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleBrand)
admin.site.register(VehicleImages)
