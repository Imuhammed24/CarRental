from django.contrib.auth.models import User
from django.db import models

from vehicles.models import Vehicle


class Reservation(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='reservations', on_delete=models.CASCADE)
    start_period = models.DateTimeField()
    end_period = models.DateTimeField()
    is_paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}\'s reservation for: {self.vehicle.brand} {self.vehicle.model} ({self.vehicle.year})'
