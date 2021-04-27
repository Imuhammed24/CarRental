import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone


class VehicleQuerySet(models.QuerySet):

    def search(self, query):
        lookup = (
            Q(brand__name__icontains=query) |
            Q(model__icontains=query) |
            Q(year__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query)
            # Q(seat_capacity__icontains=query)
        )
        return self.filter(lookup)


class VehicleManager(models.Manager):
    def get_queryset(self):
        return VehicleQuerySet(self.model, using=self._db)

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class VehicleBrand(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    CONDITION = (
        ('VERY NEAT', 'very neat'),
        ('FAIRLY NEAT', 'fairly neat'),
        ('NOT NEAT', 'not neat'),
    )
    brand = models.ForeignKey(VehicleBrand, null=True,
                              blank=True, on_delete=models.CASCADE,
                              related_name='vehicles')
    model = models.CharField(max_length=30)
    year = models.IntegerField()
    description = models.CharField(max_length=200)
    condition = models.CharField(choices=CONDITION, null=True, blank=True, max_length=200)
    colour = models.CharField(blank=True, null=True, max_length=20)
    price = models.FloatField()
    seat_capacity = models.IntegerField()
    quantity = models.IntegerField()
    availability = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=True)
    current_location = models.CharField(blank=True, null=True, max_length=20)


    objects = VehicleManager()

    def __str__(self):
        return f'{self.brand.name, self.model} ({self.year})'


class VehicleImages(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField()


class Messages(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='conversations', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'from {self.sender} to {self.receiver}'

    class Meta:
        ordering = ['timestamp']
