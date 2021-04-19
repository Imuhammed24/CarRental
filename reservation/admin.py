from django.contrib import admin
from reservation.models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'start_period', 'end_period', 'is_paid', 'user']


admin.site.register(Reservation, ReservationAdmin)
