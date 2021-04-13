from django.db import models
# from django.contrib.postgres.fields import JSONField
# from django_mysql.models import JSONField
from jsonfield import JSONField


class PaymentHistory(models.Model):
    """This class stores JSON dump from paystack."""
    email = models.EmailField(max_length=60)
    reference = models.CharField(max_length=50)
    data = JSONField()

    def __str__(self):
        return self.email
