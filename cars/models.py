from django.db import models


class Vehicle(models.Model):
    brand_name = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    seat_capacity = models.IntegerField()
    quantity = models.IntegerField()
    availability = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.brand_name, self.model}'

