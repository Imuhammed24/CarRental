from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.


class SearchQuery(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    query = models.CharField(max_length=220)
    timestamp = models.DateTimeField(auto_now_add=True)
