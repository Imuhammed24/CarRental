from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=30)


class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user}\'s profile'
