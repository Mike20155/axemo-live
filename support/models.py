from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import hashlib
import random
# Create your models here

STATUS = [
    ('Unresolved', 'Unresolved'),
    ('Resolved', 'Resolved'),
]


def encrypt():
    id =  random.randint(1, 100000000000000)
    crypt = hashlib.sha256(str(id).encode()).hexdigest()[:10]
    return crypt

# Create your models here.


class Tickets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    i_d = models.CharField(max_length=200, default=encrypt())
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=200, choices=STATUS, default='Unresolved')
    category = models.CharField(max_length=200, default='none')
    title = models.CharField(max_length=200, default='none')
    description = models.TextField(max_length=200, default='none')
    chat = models.TextField(max_length=200, default='{}')
    objects = None

    def __str__(self):
        return str(self.title)


class Contacts(models.Model):
    full_name = models.CharField(max_length=200, default='none')
    email = models.CharField(max_length=200, default='none')
    message = models.TextField(max_length=200, default='none')
    date_created = models.DateTimeField(default=timezone.now)
    i_d = models.CharField(max_length=200, default=encrypt())
    objects = None

    def __str__(self):
        return str(self.full_name)


class Inquiry(models.Model):
    full_name = models.CharField(max_length=200, default='none')
    email = models.CharField(max_length=200, default='none')
    inquiry = models.TextField(max_length=200, default='none')
    date_created = models.DateTimeField(default=timezone.now)
    i_d = models.CharField(max_length=200, default=encrypt())
    objects = None

    def __str__(self):
        return str(self.full_name)
