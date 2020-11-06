from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


STATUS = [
    ('active', 'active'),
    ('completed', 'completed'),
]


class Investments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    capital = models.DecimalField(max_digits=50, decimal_places=2)
    tx_hash = models.CharField(max_length=250, null=True)
    status = models.CharField(max_length=200, choices=STATUS, default='active')
    week = models.CharField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=250)
    date_created = models.DateTimeField(default=timezone.now)
    total_paid = models.DecimalField(max_digits=50, decimal_places=2)
    percentage = models.DecimalField(max_digits=50, decimal_places=2)
    objects = None

    def __str__(self):
        return str(self.user)
