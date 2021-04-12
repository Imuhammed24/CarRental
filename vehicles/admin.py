from django.contrib import admin
from .models import Vehicle, VehicleBrand, VehicleImages, Messages

admin.site.register(Messages)
admin.site.register(Vehicle)
admin.site.register(VehicleBrand)
admin.site.register(VehicleImages)
