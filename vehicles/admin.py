from django.contrib import admin
from .models import Vehicle, VehicleBrand, VehicleImages, Messages


class MessagesAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp', 'is_read']


admin.site.register(Messages, MessagesAdmin)

admin.site.register(Vehicle)
admin.site.register(VehicleBrand)
admin.site.register(VehicleImages)
