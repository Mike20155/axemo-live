from django.db import models


class Notifications(models.Model):
    data_type = models.CharField(max_length=50, null=True)
    data = models.CharField(max_length=5000000, null=True)
    objects = None

    def __str__(self):
        return str(self.data_type)
